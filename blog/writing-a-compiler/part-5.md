# Writing a Compiler (Part 5): Defining AST Nodes

This is where things start to get juicy, where we actually start to define the
structure of our programming language in term of code!

Since there is a lot of code to cover, it would be best to reference the
[source](https://github.com/dosisod/write-a-compiler/blob/200e29beb0b870415e8ce823904ccf131eff141f/wac/ast/nodes.py)
and [test](https://github.com/dosisod/write-a-compiler/blob/200e29beb0b870415e8ce823904ccf131eff141f/test/test_ast_nodes.py)
files as you read along.

Let's begin!

## Before We Begin ...

I briefly mentioned dataclasses in part 2 of this series, but I think it would be best to
go into more depth with it before we dive deeper. With dataclasses, we can define very concise,
very rich classes, primarily using types. What does this look like in practice?

```python
@dataclass
class Person:
    name: str

@dataclass
class Baker(Person):
    profession: str = "baker"

@dataclass
class Plumber(Person):
    profession: str = "plumber"

alice = Person(name="alice")
assert isinstance(alice, Person)

bob = Baker(name="bob")
assert isinstance(bob, Person)
assert isinstance(bob, Baker)

charlie = Plumber(name="charlie")
assert isinstance(charlie, Person)
assert isinstance(charlie, Plumber)
```

As you can see, we can create very nice, strongly typed class heiarchies very quickly.
This is super important when we actually start to define our AST nodes.

It is really nice that we don't have to make our own boilerplate `__init__` method, though
we run into trouble when we want to customize `__init__`. Luckily there is a way
to change this, and that is with the `field` method:

```python
@dataclass
class Person:
    name: str
    is_person: bool = field(True, init=False)

alice = Person(name="alice")

bob = Person(name="bob", is_person=False)  # error
```

In this example, we get an error when we try to pass `is_person`, since `init=False` will
remove it from the `__init__` method.

With that out of the way, I think we can jump into:

## The AST Nodes

### The Base Nodes

These are the root/base nodes, the core of our AST tree:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Tuple


class Node:
    pass


class ExprType:
    pass
```

The first part is just our `import`s, nothing too special here.
The `Node` and `ExprType` classes are empty base nodes which we will extend off of later.

### The Types

One of the most important parts of our AST is the ability to represent complex types.
We could of course use `type` to represent our types, though `type` is very lax, allowing us
to store pretty much anything in it. Instead, we do something like this:

```python
@dataclass
class SingleExprType(ExprType):
    type: type


@dataclass
class TupleExprType(ExprType):
    type: Tuple[ExprType, ...]
```

These `SingleExprType` and `TupleExprType` classes extend off of `ExprType`,
and basically give us wrappers around the built-in Python types.

### The Basic Expressions

Expressions are usually the denses part of an AST.
Everything from literals (`123`, `true`, etc), function calls, binary expressions, and so on.
These next few are terminal expressions, meaning they are a single value, usually a single
token.

```python
@dataclass
class Expr(Node):
    rtype: ExprType = field(init=False)
```

This is the root node for our expressions (numbers, results of equations, function call results, etc).
We use `init=False` because we won't be setting this in our `__init__` methods, but in the body
of the classes which extend off of this one.

`rtype` represents the "return type" or "resulting type" when this expression is evaluated.

---

```python
@dataclass
class IntExpr(Expr):
    rtype = SingleExprType(int)
    value: int


@dataclass
class BoolExpr(Expr):
    rtype = SingleExprType(bool)
    value: bool


@dataclass
class FloatExpr(Expr):
    rtype = SingleExprType(float)
    value: float


@dataclass
class StrExpr(Expr):
    value: str
    rtype = SingleExprType(str)
```

These next few nodes just represent common expression nodes which we will probably use all the time,
such as our `int`s and `bool`s. They have an `rtype` which represents the type of the expression,
and a `value`. Since these are literal expressions (ie, `1`, `"hello world"`, etc), we know the
value ahead of time, and can store it directly.

---

```python
@dataclass
class IdentifierExpr(Expr):
    rtype: ExprType = field(init=True)
    name: str
```

Now we get to the identifier, which is something like `x` or `y`.
Note that we now use `init=True`, which means we have to define the `rtype` when we construct an `IdentifierExpr`.
We also have a `name` which is pretty self-explanitory.

---

```python
@dataclass
class TupleExpr(Expr):
    rtype: TupleExprType = field(init=True)
    values: Tuple[Expr, ...]

    @classmethod
    def of(cls, *args: Expr) -> TupleExpr:
        return cls(
            TupleExprType(tuple(expr.rtype for expr in args)),
            args,
        )
```

The `TupleExpr` is a bit more complex, only because we have this special `of` helper method.
A `tuple` is an immutable container of zero or more expressions, such as `(1, 2, 3)`, `(1,)`, or just `()`.
To see why we need this `of` method, let's see what it would look like to create a `TupleExpr` with and
without the `of` method:

Without `of`:

```python
value1 = IntExpr(123)
value2 = FloatExpr(3.14)
t = TupleExpr(
    rtype=TupleExprType(value1.rtype, value2.rtype),
    values=(value1, value2)
)
```

With `of`:

```python
value1 = IntExpr(123)
value2 = FloatExpr(3.14)
t = TupleExpr.of(value1, value2)
```

Isn't that nice? Basically, since we know the `rtype` of `value1` and `value2`, we can pull those out
and use them to create our new `TupleExpr`.

### The Complex Expressions

These are going to be our binary expressions (ie, `1 + 2`), and unary expressions (ie, `not true`).
They require a little bit more setup:

```python
class BinaryExprOper(Enum):
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    POWER = auto()
    EQUALS = auto()
    LESS_THEN = auto()
    LESS_THEN_EQ = auto()
    GREATER_THEN = auto()
    GREATER_THEN_EQ = auto()

    def is_bool_like(self) -> bool:
        oper = type(self)

        return self in (
            oper.EQUALS,
            oper.LESS_THEN,
            oper.LESS_THEN_EQ,
            oper.GREATER_THEN,
            oper.GREATER_THEN_EQ,
        )
```

`BinaryExprOper` is an enum which contains all of the binary operators we support. There is also a
`is_bool_like` method which tells us whether an operator results in a boolean or not. To see why this
is important, lets take a look at an example:

```python
# What should the resulting type of this expression be?
1 + 2

# And this?
1.0 + 2.0

# What about this?
1 < 2
```

Answer: `int`, `float`, and `bool`. Notice the `<` operator always results in a `bool`, but the result
of the `+` operator depends on the types of the expressions to the left-hand and right-hand side of the `+`.

---

```python
@dataclass
class BinaryExpr(Expr):
    rtype: ExprType = field(init=True)
    lhs: Expr
    oper: BinaryExprOper
    rhs: Expr

    @classmethod
    def of(cls, lhs: Expr, oper: BinaryExprOper, rhs: Expr) -> BinaryExpr:
        type = SingleExprType(bool) if oper.is_bool_like() else lhs.rtype

        return cls(type, lhs, oper, rhs)
```

This is the expr class that corresponds to the `BinaryExprOper`.
We have an `rtype` (user defined), a left-hand side (`lhs`), an `oper`, and a right-hand side (`rhs`).

Again, we have an `of` method to allow us to pass 2 expressions, an operator, and get back a nice `BinaryExpr`:

```python
BinaryExpr.of(IntExpr(1), BinaryExprOper.ADD, IntExpr(2))
```

Since we pass in a non-bool operator, `ADD`, the resulting type is `SingleExprType(int)`.

---

```python
class UnaryExprOper(Enum):
    NEGATIVE = auto()
    NOT = auto()

    def is_bool_like(self) -> bool:
        return self is type(self).NOT


@dataclass
class UnaryExpr(Expr):
    rtype: ExprType = field(init=True)
    oper: UnaryExprOper
    rhs: Expr

    @classmethod
    def of(cls, oper: UnaryExprOper, rhs: Expr) -> UnaryExpr:
        type = SingleExprType(bool) if oper.is_bool_like() else rhs.rtype

        return cls(type, oper, rhs)
```

The unary expressions are pretty much the same as the binary ones, except that there are a lot less
unary operators we have to account for.

### The Statements

In most programming languages, statements are constructs which don't return a value, such as a function
declaration, or an if statement. In F# though, most things are an expression, including if statements.
To make things easier, we will create statements to represent these constructs, but still treat them as
if they are expressions:

```python
class Stmt:
    pass


@dataclass
class VarDefStmtExpr(Stmt, Expr):
    name: str
    expr: Expr


@dataclass
class ModuleDefStmtExpr(Stmt, Expr):
    name: str
    stmts: Tuple[Stmt, ...]
```

As you can see, `VarDefStmtExpr` and `ModuleDefStmtExpr` are both statements and expressions.

A variable definition is basically a name attached to an expression, so that is how we represent it.
A module is basically a name, and a bunch of statements, like so:

```fsharp
module m =
  let name = "bob"

  let b = 2

Console.WriteLine m.name

// prints "bob"
```

## Testing It All

Of course we wouldn't forget to write our tests, would we? I won't go over all the tests here,
but I urge you to look at them
[here](https://github.com/dosisod/write-a-compiler/blob/200e29beb0b870415e8ce823904ccf131eff141f/test/test_ast_nodes.py)
for examples of how the classes we defined are supposed to be used.

## Fin

That's it! We will almost certainly be changing this over time, adding more, changing what doesn't
work, etc. This will work well for now though.

The next step is going to be mapping our token stream into AST nodes!

[[prev](./part-4.html)]
