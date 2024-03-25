# The future of Python looks fast, and corporate

I've been noticing a tend in the Python ecosystem recently:

1. You create a project that people like
2. Figure it might be profitable
3. Turn it into a legal entity (usually a Delaware C Corp)

Here are some recent examples of this:

## Ruff

[Ruff](https://github.com/astral-sh/ruff), in it's own words, is "an extremely fast Python linter, written in Rust".
It has gained a lot of popularity by being "10-100x faster than existing linters" such as flake8, one of the
most popular Python linters.

[The first commit](https://github.com/astral-sh/ruff/commit/0d8e4bd6e9580a2484fa68c45cb3569e0815ac3f) was on August 9th, 2022.

On November 4th, 2022, "Astral Software Inc" was formed in the State of Delaware [^1].
The Ruff project had about 2.5k stars by this point. Astral is focusing on building
fast Python tooling, according to their [website](https://astral.sh/), and if Ruff
is any indication, I believe it.

## Pydantic

For anyone building web apps, [Pydantic](https://github.com/pydantic/pydantic) needs no introduction.
Pydantic is a model validation library that is used to create nice, type-safe models for Python
applications, typically web apps.

[The first commit](https://github.com/pydantic/pydantic/commit/a8e844dad56388522ddbaa68a3285570d5cef7b3) was on May 3rd, 2017.

On December 14th, 2022, "Pydantic Services Inc" was formed in the State of Delaware.
The Pydantic project had about 11.5k stars by this point. Their mission:

> First, we built a data validation library that developers love.

> Next, we're building cloud services that developers will love.

Currently Pydantic is written in plain Python, though Pydantic v2 will be written in,
you guessed it, Rust, and will be "5-50x faster than v1".

## Mojo

If you're keeping up with the Python news you've probably heard about [Mojo](https://www.modular.com/mojo).
Mojo is a Python super-set that is geared towards AI, and boasts a 35,000x speedup compared to Python [^2].

Since Mojo isn't open source yet, there isn't any star metrics to go off here.

On October 5th, 2017, "Modular, Inc" was formed in the State of Delaware [^3].
2017 seems like a long time ago considering we are just now hearing about it, but the
ball only seemed to start rolling on February 2nd, 2022, when Modular foreign qualified
in the State of California. A couple months later, in April, Modular got ahold of the
[modular.com](https://modular.com) domain [^4].

Since Mojo isn't open source, there is no way to tell whether it is written in Rust or not.
Given that it is built on top of MLIR/LLVM it will probably be written in C++ or Rust [^5].
I'd be curious to see how Mojo compares to CPython when it finally gets open sourced.


## And many more to come

These are just a few high profile examples of projects that are incorporating. As a fledgling CEO myself [^6]
I am finding it very interesting to learn about business structures and how that ties in with
the software ecosystem as a whole. As a programmer, I find it ironic that the future of Python
is less about Python itself, and more about how we can use other tools and languages to make Python
faster for everyone else.

---

[^1]: Apparently "Astral Software Inc" was already formed in Delaware in 1995. It closed at some point
(when I don't know), and the new "Astral Software Inc" was formed in 2022. Just a fun tidbit I found in my research.

[^2]: If you want a deep dive into how the Mojo team is doing this, watch [this podcast](https://youtu.be/pdJQ8iVTwj8)
with Lex Fridman and Chris Lattner.

[^3]: I gotta say, Modular Inc is a sick name for a company. Surprised it wasn't taken already.

[^4]: Previously the domain was owned by "Reflex Publishing Inc". You can view the site [here](https://web.archive.org/web/20220401015755/https://www.modular.com/).

[^5]: While Clang/LLVM is written in C++, LLVM has bindings for many languages, including Rust (which actually makes heavy use LLVM),
hence why I believe Mojo will probably be written in C++ or Rust (or perhaps a mix of both).

[^6]: [cicada.sh](https://cicada.sh)
