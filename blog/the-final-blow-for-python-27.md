# The Final Blow For Python 2.7

Despite the fact that Python 2.7 was sunset in 2020 [^1], many library maintainers
chose to continue to support Python 2.7 users [^2]. That is starting to change, though.

I've recently noticed that many projects are just now dropping support for Python 2.7,
some even dropping support for Python 3.5 and below (more on that later).
Here is a list of some of the more popular libraries and tools that have recently
dropped support for Python 2:

* [Mypy](https://github.com/python/mypy/pull/13135), July 26th
* [Pyflakes](https://github.com/PyCQA/pyflakes/pull/707), June 12th
* [Attrs](https://github.com/python-attrs/attrs/pull/936), March 21st

## Why This Is Good

Dropping support for Python 2 has a lot of added benefits:

* Less code to maintain
* Faster code
* Smaller attack surface
* Less bugs
* Ability to use new language features
* Happier maintainers

People who refuse to upgrade (or cannot upgrade) will be stuck with these older
versions, and us Python 3 peeps will get the latest and greatest features, but
without the burden of having to support both Python 2 and 3. The main improvement
that users will see is better type annotations. Sure, you could use type comments
or stub files, but it just cannot compete with type info that is in the source
itself.

## Why Now?

A lot has been added in recent versions of Python:

Python 3.9 allows for using `list[int]` instead of `List[int]` (notice the lower-case
L), meaning less imports in each of your files. This also applies to all the built-in
datatypes, including `dict`, `set`, and so on.

Python 3.10 adds many cool features, one of the most useful being
[pattern matching](https://peps.python.org/pep-0636/#appendix-a). In addition, 3.10
added type unions, the ability to create multiple context managers with a single
`with` block, and better error messages.

Python 3.11, although still in [beta](https://docs.python.org/3.11/whatsnew/3.11.html),
has some killer improvements, such as being ["10-60% faster than Python 3.10"](https://peps.python.org/pep-0664/#features-for-3-11),
getting a new TOML standard library, a dedicated `Self` type, and very nice error messages
(I think Rust has become a driving force for what error messages should be).

With all this in mind, its no wonder that maintainers are wanting to use these features
in their code, and to leave Python 2 in the past.

## What About Python < 3.5?

What I find even more interesting is the
dropping of support for Python 3.5 and lower. If I had to guess, that is due to the
introduction of type annotations in version 3.6. Python is really going all out for type
annotations, and as a result, more and more people are using them in their projects.

## Fin

Python is going through some exciting changes! The ecosystem surrounding it is large
and ever-changing, but in general, is going in a good direction. I think that Python
will continue to see widespread adoption, especially the newer versions of Python.

---

[^1]: [](https://www.python.org/doc/sunset-python-2/)

[^2]: When I say "supporting", I am also talking about tools that parse Python 2 code,
even if the tools themselves are written in Python 3.
