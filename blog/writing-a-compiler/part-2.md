# Writing a Compiler (Part 2): Tokenizing

The first stage of any compiler is the tokenizer. A tokenizer will split up
a string of code into "tokens", where each token represents the smallest,
yet still meaningful chunk of code. A tokenizer might take in some code like
this:

```
x + 1
```

And convert it into something like this:

```json
[
  { "contents": "x", "type": "identifier", "line": 1, "column": 1 },
  { "contents": "+", "type": "operator", "line": 1, "column": 3 },
  { "contents": "1", "type": "number", "line": 1, "column": 5 },
]
```

Each element in this array is a token, and has some basic information about it,
such its contents, type, and the line/column it is on.

The code for this blog is viewable [here](https://github.com/dosisod/write-a-compiler/tree/part2).

## What is a Token?

Lets start by defining what a token is:

In `wac/parse/token.py`:

```python
from enum import Enum, auto
from typing import Optional

class TokenType(Enum):
    IDENTIFIER = auto()
    WHITESPACE = auto()
    NEWLINE = auto()

@dataclass
class Token:
    content: str
    line: int
    column: int
    type: Optional[TokenType] = None
```

A basic token will have the `contents` of the token, the `line` and `column`
it is on, and the `type` of said token. The type is allowed to be optional, since
we won't know the type of the token until later.

We are using a [dataclass](https://docs.python.org/3/library/dataclasses.html)
for `Token`. This allows for us to write just the outline of the class, and all of our
boilerplate `__init__`, `__eq__`, etc. methods will be created automatically.

To verify that what we have currently is working, lets add the following test
in `test/test_tokenizer.py`:

```python
from wac.parse.token import Token, TokenType

def test_create_token():
    token = Token("hello", 1, 2)

    assert token.content == "hello"
    assert token.line == 1
    assert token.column == 2
    assert not token.type


def test_create_token_with_type():
    token = Token("hello", 1, 2, TokenType.IDENTIFIER)

    assert token.content == "hello"
    assert token.line == 1
    assert token.column == 2
    assert token.type == TokenType.IDENTIFIER


def test_token_compare():
    assert Token("hello", 1, 1) == Token("hello", 1, 1)
```

And run it with `pytest`. We shouldn't get any errors.

## Creating Location Info

Next up is taking a string of code, and assigning location info to each of the
characters. The logic is pretty simple:

* Start at line 1, column 1
* Emit a tuple containing the current char, line, and column
* After each character, increment column by 1
* If we are on a newline character, increment line, and set column to 1

We might change this later, but this should cover all of the important use
cases.

We will create a [NamedTuple](https://docs.python.org/3/library/typing.html#typing.NamedTuple)
to store our new `LocationInfo` data structure:

```python
from typing import NamedTuple

class LocationInfo(NamedTuple):
    char: str
    line: int
    column: int
```

Now we will create a function to take in some code, and using the logic we
defined above, return a generator which will emit our location info:

```python
def generate_location_info(
    code: str,
) -> Generator[LocationInfo, None, None]:
    line = 1
    column = 1

    for c in code:
        yield LocationInfo(c, line, column)

        if c == "\n":
            line += 1
            column = 1

        else:
            column += 1
```

The `-> Generator[...]` part is return type annotation, which tells mypy (and
your intellisense if you're using VSCode) what the `generate_location_info` function
is actually returning.

We will test the functionality of our new function in the existing `test_tokenizer.py` file:

```python
from wac.parse.token import generate_location_info

def test_generate_location_info():
    locations = list(generate_location_info("a\nbc\ndef"))

    assert locations == [
        ("a", 1, 1),
        ("\n", 1, 2),
        ("b", 2, 1),
        ("c", 2, 2),
        ("\n", 2, 3),
        ("d", 3, 1),
        ("e", 3, 2),
        ("f", 3, 3),
    ]
```

## Generating the Tokens

Now that we have the ability to get location info for each of the characters in
our string, we can start to group similar characters and make tokens!

```python
from itertools import groupby
from typing import Generator, List, Optional

def char_to_token_type(c: str) -> Optional[TokenType]:
    if c == "\n":
        return TokenType.NEWLINE

    if c.isspace():
        return TokenType.WHITESPACE

    if c.isalpha():
        return TokenType.IDENTIFIER

    return None


def tokenize(code: str) -> List[Token]:
    def create_token(token_info):
        contents = "".join([info.char for info in token_info])

        return Token(contents, token_info[0].line, token_info[0].column)

    location_info = generate_location_info(code)

    grouped = groupby(
        location_info,
        lambda info: char_to_token_type(info.char),
    )

    return [create_token(list(group[1])) for group in grouped]
```

`char_to_token_type` will take a single char, and try and figure out what kind
of token type it is. We will add to this later, but this should be good for now.

`tokenize` is a little more complex, but not too much. Basically, we start out by
generating the location info, figuring out the token type (using the `lambda`
function), and group all the tokens which have the same token type. An example of
what `groupby` does:

```python
>>> from itertools import groupby

>>> nums = [1, 2, 3, -1, -2, 10, -10]

>>> groups = groupby(nums, lambda x: x > 0)

>>> [(group[0], list(group[1])) for group in groups]
[(True, [1, 2, 3]), (False, [-1, -2]), (True, [10]), (False, [-10])]
```

What we get back is an array of tuples, each tuple having the return value of
our lambda on the left, and the grouped values which match that lambda's return
value on the right.

Once we have our location info all grouped up, we loop through each group,
adding up all the `char`'s, taking the `line`/`column` info of the first
location info tuple, and creating a token from that.

Here are the associated tests for above:

```python
from wac.parse.token import Token, tokenize

def test_tokenize_single_token():
    tokens = tokenize("hello")

    assert tokens == [Token("hello", 1, 1)]


def test_tokenize_2_tokens():
    tokens = tokenize("hello\n")

    assert tokens == [Token("hello", 1, 1), Token("\n", 1, 6)]


def test_tokenize_many_tokens():
    tokens = tokenize("hello world")

    assert tokens == [
        Token("hello", 1, 1),
        Token(" ", 1, 6),
        Token("world", 1, 7),
    ]


def test_tokenize_unknown_token():
    tokens = tokenize("+")

    assert tokens == [Token("+", 1, 1)]
```

## Next Steps

In the next blog we will further improve upon our tokenizer, and start actually
classifying the tokens based on their contents.

[[prev](./part-1.html)]
[[next](./part-3.html)]
