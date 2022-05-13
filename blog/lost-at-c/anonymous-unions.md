# Lost at C: Anonymous Unions

This is the first installment of a new series, "Lost at C", where I go over
obscure language features, historical mishaps, and other interesting parts
about the C programming language.

## What are unions?

A union is a data structure that can store many different data types, but
only one at any given time. Let me explain:

```c
union Number {
    int i;
    float f;
    double d;
};
```

Here we define a union called `Number`. It can store an `int`, `float`, and
a `double`. The size of `Number` will be the size of the biggest field in the
union, which will be the `double`.

To actually use it is pretty simple:

```c
union Number i = { .i = 1234 };
union Number f = { .f = 3.14f };
union Number d = { .d = 1.414 };

printf("%i\n", i.i);
printf("%f\n", f.f);
printf("%lf\n", d.d);
```

When compiling, we get the following result:

```
1234
3.140000
1.414000
```

Now, what happens if we use a different field then the datatype that we expect?

```c
printf("%i\n", d.i);
printf("%f\n", i.f);
printf("%lf\n", f.d);
```

Compiling and running:

```
1992864825
0.000000
0.000000
```

Was that what you where expecting?

Basically, to use a union correctly, we need a way of identifying what the
state of the union is in, so that we can use it correctly:

```c
struct NewNumber {
    int state;

    union {
        int i;
        float f;
        double d;
    } num;
};
```

Now instead of using `Number`, we can use `NewNumber`, which will allow
for us to set the `state` field. Now we can set/get the `state` field,
and based on the results, properly handle the data in the `num` union:

```c
struct NewNumber age = {
    .state = 0,
    .num = { .i = 1234 }
};

// call like so:
if (age.state == 0) printf("%i\n", age.num.i);
if (age.state == 1) printf("%f\n", age.num.f);
if (age.state == 2) printf("%lf\n", age.num.d);
```

Here we are using a simple `int` to describe the data being stored in the
union. In practice, we probably want to use an enum to better signify
what state is which.

Note that the declaration of the union is slightly different as well. There
are many different ways of declaring a union:

```c
// version 1
union X { };

// version 2
union X { } Y;

// version 3
union { } Y;

// version 4
union { };
```

1. This is what we used originally. This will create a union with a type of `X`, and can be declared via `union X x = ...`
2. Same as 1, except we also create an instance of the union, and call it `Y`
3. This union is used primarily in structs, since we don't need the type, just access to the instance `Y`.
4. This is the anonymous union, which we will explain below!


## The anonymous union

One of the annoying things about our `NewNumber` struct is that we have to
access the number values via this `.num` field, which feels clumsy. If only
there was a way to have the fields inside of the union just become part of
the struct. Well, that is were anonymous unions come in!

```c
struct FinalNumber {
    int state;
    union {
        int i;
        float f;
        double d;
    };
};
```

Now we can use the number like so:

```c
struct FinalNumber fn = {
    .state = 0,
    .i = 1234
};

printf("%i\n", fn.i);
```

## What is this good for?

This is really good for cutting down on the size of structs when they have many
states, but can only be in one at a time. For example, a `Node` struct, which
has a union to pointers containing metadata about different `Node` types:

```c
struct Node {
    enum NodeType type;
    union {
        struct VariableNode *var;
        struct DefinitionNode *def;
        struct ExpressionNode *expr;
    };
};
```

## The cons

One of the big drawbacks of using a union is that you can get into weird issues
if you don't properly check the state before using the data in the union. For
example:

```c
struct Person {
    union {
        const char *name;
        char *dynamic_name;
    };

    unsigned age;
};
```

The person has a `name`, which is a `const char *`. It cannot be touched. But
you can also access `name` via `dynamic_name`, which is not `const`. This means
that if you try to access a name using `dynamic_name` which was set via `name`,
you will (probably) run into some trouble.

Note that this still could be useful for being able to declare people with
names that aren't heap allocated, and not need to use `strdup`. Still, you
need a way to know whether it was heap allocated or not.

## Final Thoughts

All in all, anonymous unions (and unions in general) are a really great
language feature when used properly, but can cause some major headaches if used
incorrectly.
