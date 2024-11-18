# The Perfect Programming Language

I know a lot of different programming languages, I've even built my own, and as
a result, I have some opinions about what makes a programming language good or bad.
I don't think that there exists a "perfect language", but there are bits and pieces of
existing languages, which when combined, could be really interesting when put together.

Also, when I say "programming language", I will also delve into the compiler of said
language, the runtime environment, and so on [^1].

Let's begin! In no particular order...

## Pattern Matching

If you haven't used pattern matching before, you should give it a try! Languages
like Rust, F#, and Python (as of version 3.10) have pattern matching. They allow
you to succinctly match based off of the structure of your data, while also
destructuring it for use in the case body. For example, in Python:

```python
point = (10, 42)

match point:
    case (x, _) if x < 0:
        print("x is negative")

    case (_, y) if y < 0:
        print("y is negative")

    case (x, y):
        print(f"x is {x}, y is {y}")

    case _:
        print("point is invalid")
```

This is a trivial example, but pattern matching can do a whole lot more than what
I just showed you. Read
[this (Python)](https://peps.python.org/pep-0636/) and
[this (Rust)](https://doc.rust-lang.org/rust-by-example/flow_control/match.html) for
better examples of how pattern matching works in Python and Rust.

## Static Types

The jury is in, and static types are cool again. This is evident given the rise in popularity
of TypeScript, and type annotations in Python [^2]. Using dynamic languages are great, and the
added safety of type information makes them not a total pain to use.

TypeScript's type system is especially mature, and is almost an entire programming language
in and of itself. Take a look at the [Type Challenges](https://github.com/type-challenges/type-challenges)
repo on GitHub for some examples of what I'm talking about.

In general, better type systems allow for more safety when dealing with your data, and
allow for leveraging types to do your validation for you, instead of having to do it
all by yourself.

## Trailing Types

Although not 100% required, trailing types are, IMO, much more readable compared
to traditional ones:

```c
// traditional types
int x = 123;  // int x is equal to 123
int f();      // int returned by function f
```

```typescript
// trailing types
x: int = 123;  // x is an int equal to 123
f: () => int;  // f is a function returning an int
```

As you can (hopefully) tell, the second group looks much more readable: It reads left to
right, and the function/field names are both on the left, with they type info to the right.

## Functional Programs With Automatic Concurrency

Functional programming is on the rise, along with employing functional programming methodologies
in existing languages. I can't even remember the last time I wrote a class
in JavaScript. In JavaScript, using `filter`, `map` and `reduce` feel so
much better then looping over things with for-loops.

In addition, lots of languages are going immutable by default, such as Rust and F#.
Being immutable by default doesn't automatically make a language functional, but it
is a step in the right direction.

We are seeing wider adoption of languages like Haskell, Clojure, and F#, but none of
them have hit the mainstream. I think we are one step away from closing this gap, and
that is:

We must get rid of [function colors](https://journal.stuffwithstuff.com/2015/02/01/what-color-is-your-function/).

TL;DR, red and blue functions represent async and non-async functions. We have special
keywords we use to call these functions, and there are certain restrictions on how
you are able to call them and so on.

What would be great (and maybe impossible) is a language which is automatically able to
run your program concurrently.

This is really hard. You need to take into account the lifetime of all the variables
passed to the function, whether the function has side effects or not, and so on.
But, assuming you solve this, you will be able to achieve very fast programs without
having to think about async/await/threads. One of the biggest pros of C# is their very
mature async/await ecosystem. Python does support async, but I have found it a little bit
more clunky to use compared to C#. Having the ability to automatically run long running
tasks in the background would be a real game changer, though achieving it might be an
impossible feat.

## Domain Specific

We have seen the rise and fall of many programming languages. Some try to be general
purpose, which means it must generalize to all use cases, which can be hard. Some
languages are domain specific, and solve a particular problem very well. I would say
that the general purpose programming language field has sorta burned out. We have enough
of them already, and they already get the job done for the most part. We don't really need
any more.

What we need are small, purpose-built languages that do one thing really well [^3]. I would
much rather pickup and start using a DSL with only the features that I need, as opposed
to a general purpose language which has too many features, and not the ones I need.

Also, an entire language meant to cater a specific domain will (probably) feel a lot
better then using an library in an existing language (if done correctly).

## Uniform Style

Languages that don't specify a style guide inevitably end up with complex linting/formatting
tools, such as C/C++/JavaScript. These languages have a "common" style associated with them,
but still allow for a lot of wiggle room.

Tools like [black](https://github.com/psf/black), [gofmt](https://go.dev/blog/gofmt),
and [rustfmt](https://github.com/rust-lang/rustfmt) are opinionated formatters that
standardizes the look of your code for you. It might not be what you prefer, but having
an easy way to format your code based on an agreed upon format is really nice.

The less time we spend on configuring linters, the more time we have to actually write code!

## Elegant

This is very subjective, and hard to define, but a well written program should reward you
with something which is elegant and easy to read, easy to understand, distilled to its truest
form.

## Fin

That's it! I am probably forgot a lot of important categories, but these are the ones I came
up with off the top of my head.

I don't think a language can exist which has all of these features, but I can dream, can't I?

---

[^1]: Languages don't exist in a vacuum, they exist amongst their compilers,
the environments they run in, and the use cases people find for the language.

[^2]: Obviously I am excluding popular languages which are already statically typed, such
as C++, C#, Java, and so on.

[^3]: See also, [Unix Philosophy](https://en.m.wikipedia.org/wiki/Unix_philosophy).
