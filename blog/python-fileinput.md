# Python's `fileinput` Module

You think you know Python, and then you stumble across the [fileinput](https://docs.python.org/3/library/fileinput.html) module:

> [fileinput] iterates over the lines of all files listed in `sys.argv[1:]`, defaulting to `sys.stdin` if the list is empty.
> If a filename is `'-'`, it is also replaced by `sys.stdin`...

This is so helpful, how have I never heard of this module before?

I've always just iterated over `sys.argv[1:]` directly and opened all the files manually, not even handling `-` because it would be
another condition I didn't feel like testing. This little bit of boilerplate reduction makes quick file IO much nicer IMO.
You can even modify files inplace by simply printing to stdout (assuming you set the `inplace` keyword).

This made me think, what CLI tasks could this be used for?

## `cat` clone

Recreating `cat` is trivial:

```python
import fileinput as f

for x in f.input():
  print(x, end="")
```

Lets create some test data:

```shell
$ echo "abc123" > a
$ echo "bbbbbb" > b
$ echo "c45678" > c
```

Then run our `cat.py` program:

```shell
$ python3 cat.py a b c
abc123
bbbbbb
c45678
```

What about stdin?

```shell
$ echo "hello" | python3 cat.py -
hello
```

Amazing!


## `grep` clone

Recreating `grep` is also pretty trivial since `fileinput` is line based and keeps track of the current file:

```python
import sys
import re
import fileinput

PATTERN = re.compile(sys.argv.pop(1))

for line in fileinput.input():
    if PATTERN.search(line):
        print(fileinput.filename(), line, sep=":", end="")
```

Running:

```shell
$ python3 grep.py c a b c
a:abc123
c:c45678
```

Our basic `grep.py` program mimics `grep` pretty well, except all the missing flags,
and of course, the color.


## `grep` clone (with color)

I'm getting a bit carried away now, but adding color support to our little `grep` clone is easy enough:

```python
import fileinput
import os
import re
import sys

PATTERN = re.compile(sys.argv.pop(1))

GREP_COLORS = os.getenv("GREP_COLORS", "ms=01;31:mc=01;31:sl=:cx=:fn=1;34:ln=32:bn=32:se=0")
COLORS = dict(x.split("=") for x in GREP_COLORS.split(":"))

RESET = "\x1b[0m"

for line in fileinput.input():
    if PATTERN.search(line):
        filename = f"\x1b[{COLORS['fn']}m{fileinput.filename()}{RESET}"
        line = PATTERN.sub(f"\x1b[{COLORS['mc']}m\\1{RESET}", line)

        print(filename, line, sep=":", end="")
```

Running the same command as above gives us the following colorized output:

<span style="color:#00f">a</span>:ab<span style="color:#f00">c</span>123
<br>
<span style="color:#00f">c</span>:<span style="color:#f00">c</span>45678

## Fin

That's all I got for now. The `fileinput` module is pretty useful for line based file operations,
though if you need to read whole files at once, you're probably better off with iterating over `sys.argv[1:]`
like usual.
