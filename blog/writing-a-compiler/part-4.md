# Writing a Compiler (Part 4): Designing the Language

One of the first things you do when you build a programming language is you
figure out what you want it to look like: How is it going to *feel*? What do
you want the code to *look* like? What [paradigm](https://en.wikipedia.org/wiki/Programming_paradigm)
will it be in? What differentiates your language from the rest?

When you are making your first language, it is a lot easier to take from an existing language,
since they have gone through all the hard work of designing it for you.

For this series, we will create an [F#](https://docs.microsoft.com/en-us/dotnet/fsharp/tour)-like
language. It won't have all of the fancy frills, just the bare minimum for us to call it
a "real" programming language, something that is actually "useful".

> For the purposes of our language, we will consider "useful" as being able to communicate with
> a C library. Any feature that our language cannot support, a C function could be created as a work-around.

The reason I am choosing F# is it is a very simple, functional language. The language constructs
we need to support are very small, and the parsing of F# (and similar functional languages) is pretty
straight-forward.

## What We Are Going To Build

Although subject to change, this the basic functionality which our language will support:

```fsharp
// This is a comment!

let num = 123
let pi: double = 3.1415

println "Hello, World!"

let square x = x * x
let addN x y = x + y

let chainExample = 3 |> square |> addN 2

let intTuple = (1, 8, 3, 4, -7, 0, 2)

if num = 123 then
  println "num is 123"
else
  println "num is not 123"

[<Import("libwhatever.so")>]
extern cFunc()
cFunc ()

module m =
  let helloWorld () = println "Hello, world!"

m.helloWorld ()
```

So now what?

## Breaking It Down

Basically, we need to break up these lines of code into statements and expressions.
An expression is something that returns a value, such as a numeric literal, a function call,
or a variable. A statement is something that doesn't return a value, like a variable declaration,
module declaration, if statement, and so on.

> F# *does* actually support `if` statements which
> return an expression, basically making it a ternary operator. We probably won't support this,
> though that might change in the future.

### Expressions

Let's start by defining what an expression is. Expressions are at the heart of all programming
languages, and are one of the hardest part to get right. An expression node will (probably)
have the following fields:

*Expression Node*:

| Field | Type | Description |
|------|------|-------------|
| `lhs` | `Expression` (optional) | Left-hand-side of expression (in the case of binary/unary operator) |
| `rhs` | `Expression` (optional) | Right-hand-side of expression (same as `lhs`) |
| `oper` | `ExpressionOperator` | The operator that this expression is (ie, `+`, `-`, `FuncCall`, `Literal` |
| `value` | `Any` (optional) | Value of the expression, in the case of a terminal expression, such as a literal |
| `type` | TBD | Type of the expression |

The `lhs` and `rhs` are only needed for binary operators, such as `+`, `-`, and so on. In the example below:

```
(1 + 2) * 3 + 4
```

We would get an expression tree somewhat similar to this:

```

         +
        / \
       *   4
      / \
     +   3
    / \
   1   2

```

As you can see, nodes `1`, `2`, `3`, and `4` are all terminal nodes (have no child nodes), meaning they will
have a `value` set. The `+` and `*` nodes have a lhs/rhs, so those fields will be set respectively.

### Statements

These next few nodes are pretty simple, so I will go thought them all at once:

**Variable Declaration Node**:

| Field | Type |
|-------|------|
| `name` | `str` |
| `expr` | `Expression` |

**External Declaration Node**:

| Field | Type |
|-------|------|
| `name` | `str` |
| `type` | TBD |

**Module Declaration Node**:

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | |
| `stmts` | `List[Statement]` | List of statements that make up this module |

There will also have to be a `Statement` type which includes variable, external data, and module
declarations (that way the `Module` node can have a list of sub modules/variables etc).

## That's It!

Really this blog has been just a stepping stone, something to help lay the groundwork for the next
few blogs.

Next time, we will actually flesh out these node objects, and start to turn our token stream into
AST nodes!

[[prev](./part-3.html)]
