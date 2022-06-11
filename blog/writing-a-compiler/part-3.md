# Writing a Compiler (Part 3): Classifying + Better Tokenizing

After we have some tokens that have been strung together, the next step is to
classify them, and give them more meaning. Classification in and of itself is
not super interesting or super hard, so in addition to classifying the tokens,
we will add basic parsing of comments, which will require us to make some changes
to our tokenizer.

Let's begin!

> The code used for this blog can be viewed [here](https://github.com/dosisod/write-a-compiler/tree/part3).

## Basic Token Type Classification

Let's start by adding some more token types to our `TokenType` enum:

```diff
 class TokenType(Enum):
     IDENTIFIER = auto()
     WHITESPACE = auto()
     NEWLINE = auto()
+    PLUS = auto()
+    DASH = auto()
+    ASTERISK = auto()
+    SLASH = auto()
+    POWER = auto()
+    OPEN_PAREN = auto()
+    CLOSE_PAREN = auto()
+    EQUAL = auto()
+    LESS_THEN = auto()
+    GREATER_THEN = auto()
+    DOT = auto()
+    COMMENT = auto()
```

All of these new token types (except `COMMENT`) are single-character tokens,
meaning we won't need to add a lot of code to properly classify these tokens.
Also, note that we are using `PLUS` instead of `ADD`, and `DASH` instead of
`MINUS`. Although it might be tempting to name these tokens after their uses,
things can start to get confusing when you lock a token to a specific use case.
For example: A "dash" can be used for both binary subtraction, and unary negation.
An example of that would be `1 - 2` (binary) and `- 1` (unary). By using the
ambiguous term "dash", we can refer to both operations, since we use the token
type to refer to the token, not the way the token is used.

Next we need to update our `char_to_token_type` function to handle the new
token types we just added:

```diff
 def char_to_token_type(c: str) -> Optional[TokenType]:
-    if c == "\n":
-        return TokenType.NEWLINE
+    simple_token_types = {
+        "\n": TokenType.NEWLINE,
+        "+": TokenType.PLUS,
+        "-": TokenType.DASH,
+        "*": TokenType.ASTERISK,
+        "/": TokenType.SLASH,
+        "^": TokenType.POWER,
+        "(": TokenType.OPEN_PAREN,
+        ")": TokenType.CLOSE_PAREN,
+        "=": TokenType.EQUAL,
+        "<": TokenType.LESS_THEN,
+        ">": TokenType.GREATER_THEN,
+        ".": TokenType.DOT,
+        "#": TokenType.COMMENT,
+    }
+
+    if token_type := simple_token_types.get(c):
+        return token_type
```

This will basically just match up a character like `+` to it's respective token
type. We use the [walrus operator](https://peps.python.org/pep-0572/) which allows
us to assign and use our temporary `token_type` variable in one line. We use the
`.get(c)` method instead of using `[c]` because `.get` will return `None` if the
key is not found, whereas using a subscript (`[]`) will cause a `KeyError` exception.
Not very pleasant!

When we run `pytest`, we will see that our `test_tokenize_unknown_token`
test fails, since `+` is now a recognized token type. To fix it, we change
it to something which doesn't have a token type yet:

```diff
 def test_tokenize_unknown_token():
-    tokens = tokenize("+")
+    tokens = tokenize("!")

-    assert tokens == [Token("+", 1, 1, None)]
+    assert tokens == [Token("!", 1, 1, None)]
```

## Cleanup

As we start to make our tokenizer more complex, it is important to recognize things
which won't work well in the future. Currently, the `LocationInfo` and `Token` concepts
are very similar, and so we might as well just use `Token`'s for everything.
That way we will just be grouping/merging/manipulating tokens, instead of both token and
location info objects.

Let's start by re-writing our `tokenize` function:

```python
def tokenize(code: str) -> List[Token]:
    def collapse_token(tokens):
        contents = "".join([token.content for token in tokens])

        first = tokens[0]
        return Token(contents, first.line, first.column, first.type)

    def location_info_to_token(info: LocationInfo) -> Token:
        return Token(
            info.char, info.line, info.column, char_to_token_type(info.char)
        )

    tokens = [
        location_info_to_token(info) for info in generate_location_info(code)
    ]

    grouped = groupby(tokens, lambda token: token.type)

    return [collapse_token(list(group[1])) for group in grouped]
```

Basically, once we get our location info, we immediately turn it into a token,
and then group on the token's type. This will make things easier down below.

## Comment Parsing

Now we need are going to add the ability to parse comments. These are the basic
requirements for a comment token:

* Starts with a `#` character
* Ends when EOL (end of line, newline) is reached
* Ends when EOF (end of file) is reached

To achieve this, we will write a function that will take the many tokens inside
of our comment and group them into a single "comment" token. Let's write some tests
to see what we should expect:

```python
def test_collapse_comment():
    tokens = tokenize("# hello world")

    assert tokens == [Token("# hello world", 1, 1, TokenType.COMMENT)]


def test_collapse_comment_respect_newlines():
    tokens = tokenize("# hello\n# world")

    assert tokens == [
        Token("# hello", 1, 1, TokenType.COMMENT),
        Token("\n", 1, 8, TokenType.NEWLINE),
        Token("# world", 2, 1, TokenType.COMMENT),
    ]
```

If we run our tests, we will see that the new tests that we added are not passing.
Let's write some code to fix that!

```python
def collapse_comment(tokens: List[Token]) -> List[Token]:
    out: List[Token] = []
    in_comment = False

    for token in tokens:
        if token.type == TokenType.COMMENT:
            in_comment = True

        elif in_comment:
            if token.type == TokenType.NEWLINE:
                in_comment = False

            else:
                out[-1].content += token.content
                continue

        out.append(token)

    return out
```

This (in short) loop through each token until we find a token with a `COMMENT` type.
Once we find it, we will append the contents of each token to the last token in our
`out` list (the comment token), until we reach a `NEWLINE`, or the loop ends.

And now we need to update our `tokenize` function:

```diff
     ]

+    tokens = collapse_comment(tokens)
+
     grouped = groupby(tokens, lambda token: token.type)
```

When we run our tests again, they should be passing.

## More Cleanup/Refactoring

As we mentioned before, the `LocationInfo`'s look very similar to the `Token`'s.
It would probably be best to just merge the two:

```diff
-class LocationInfo(NamedTuple):
-    char: str
-    line: int
-    column: int
-
-
-def generate_location_info(
+def generate_token_locations(
     code: str,
-) -> Generator[LocationInfo, None, None]:
+) -> Generator[Token, None, None]:
     line = 1
     column = 1

     for c in code:
-        yield LocationInfo(c, line, column)
+        yield Token(c, line, column)

 ...

-    def location_info_to_token(info: LocationInfo) -> Token:
-        return Token(
-            info.char, info.line, info.column, char_to_token_type(info.char)
-        )
+    def add_token_type(token: Token) -> Token:
+        token.type = char_to_token_type(token.content)
+
+        return token

     tokens = [
-        location_info_to_token(info) for info in generate_location_info(code)
+        add_token_type(token) for token in generate_token_locations(code)
     ]
```

And in our tests:

```diff
-from wac.parse.token import Token, TokenType, generate_location_info, tokenize
+from wac.parse.token import (
+    Token,
+    TokenType,
+    generate_token_locations,
+    tokenize,
+)

 ...

 def test_generate_location_info():
-    locations = list(generate_location_info("a\nbc\ndef"))
+    locations = list(generate_token_locations("a\nbc\ndef"))

     assert locations == [
-        ("a", 1, 1),
-        ("\n", 1, 2),
-        ("b", 2, 1),
-        ("c", 2, 2),
-        ("\n", 2, 3),
-        ("d", 3, 1),
-        ("e", 3, 2),
-        ("f", 3, 3),
+        Token("a", 1, 1),
+        Token("\n", 1, 2),
+        Token("b", 2, 1),
+        Token("c", 2, 2),
+        Token("\n", 2, 3),
+        Token("d", 3, 1),
+        Token("e", 3, 2),
+        Token("f", 3, 3),
     ]
```

Refactoring done!

## Fixing isort

Remember that isort is what we use for sorting our imports. We didn't set it up
in our first blog post, so now we need to configure it (the imports in the test
file is too long, and not being formatted correctly).

In `.isort.cfg`:

```ini
[settings]
multi_line_output=3
include_trailing_comma=true
color_output=true
```

Since we have color output, we will also need to update our `dev-requirements.txt`
file:

```diff
 click==8.0.4
+colorama==0.4.4
 coverage==6.3.2
```

> Don't forget to re-run `pip install -r dev-requirements.txt` afterwards!

Now when we run `make isort`, it will tell us if isort was successful or not, and
give us an indication of what failed. Note that it will not return a non-zero exit
code upon failure, which means our CI workflow would silently fail! We can fix this
by adding the following to our `Makefile`:

```diff
 isort:
-       isort . --diff
+       isort . --diff --check
```

That's it!

## What's Next

In the next blog post, we will discuss the general structure of our new programming
language, and how we will structure our AST nodes. After that, we will write an
AST parser to create said nodes.

[[prev](./part-2.html)]
[[next](./part-4.html)]
