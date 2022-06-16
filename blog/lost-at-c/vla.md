# Lost at C: Variable Length Array

Variable Length Array, or VLA for short, is a somewhat controversial feature
of C. As with all features of C, they can be used for good, or for bad.

So what is a VLA anyways?

## What is an Array?

Before we can understand VLA's, we need to understand arrays. Here is how you
define an array in C:

```c
int some_array[8];
```

This will create an identifier called `some_array`, which gives you a way to access
the 8 new integers created on the stack:

```c
int first = some_array[0];
int second = some_array[1]:

// or

int first_deref = *some_array;
int second_deref = *(some_array + 1);
```

In the first 2 lines, we use the subscript operator (`[]`), whereas in the next 2 lines,
we use pointer arithmetic. These forms are equivalent, though you will often see
`*some_array` used to dereference the first element of an array.

Also, you can initialize arrays like so:

```c
int some_array[8] = {0, 1, 2, 3, 4, 5, 6, 7};

// or, if all elements are zero:

int some_array[8] = {0};
```

## Drawbacks of Arrays

There are some things which C arrays cannot do, namely, once created, they cannot be resized.
Also, these arrays are created on the stack, which is significantly smaller compared to the
amount of storage available on the heap. If you use up too much stack memory, your program
might crash, or worse, not crash, and start acting erratically.

You can dynamically allocate your arrays using `malloc()`, which will store your data on
the heap instead of the stack. You can then resize your arrays using `realloc()`. This
obviously works, but now you need to manage the memory of this array:

```c
int *some_array = malloc(len * sizeof(int));
memset(some_array, 0, len);

// use array

free(some_array);
```

Surely there is a way for us to dynamically create arrays without having to manage
their memory, right?

## VLA

With C99 came the addition of Variable Length Arrays. As the name implies, the length of the
array can vary (only when initially defining it though):

```c
int some_len = 128;
int some_vla[some_int];
```

This will allocate 128 ints in the stack. Note that you cannot use an initializer with VLA's,
you will have to use `memset()`:

```c
memset(some_vla, 0, some_len);
```

## So Why Are VLA's So Bad?

Take the following example:

```c
int length = // read integer value from user
int vla[length];
```

This could become problematic if the user enters a large number, especially if this
function is called recursively, or if you are allocating an array of large structs.

Also, since the stacksize of the function is unknown, there could be some performance
degradation as a result.

## An alternative?

If you really need to use VLA's, an alternative is to use the `alloca()` function.
It is like `malloc()`, except it returns stack memory instead of heap memory:

```c
int len = 8;
int *some_array = alloca(len * sizeof(int));
memset(some_array, 0, len);
```

You might ask, isn't this just a VLA with more steps? And yes, you would be right.
But, this makes it so don't accidentally use VLA's (just make sure to enable the
`-Wvla` flag).

## VLA in Retrospect

VLA's where added in the C99 standard, and made optional in the C11 standard.
Also, use of VLA's are strongly discouraged, and they even have their own `-Wvla`
flag to warn of their use.

## Fin

Knowing what VLA's are and how they are used is important, even if you don't
use them everyday. If you do use them, just make sure to be aware of the
possible drawbacks.
