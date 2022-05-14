# Lost at C: Bool

One of the most common data types in any programming language is the boolean, giving you the
basic ability to say whether something is true or false. C is
special though, in that there isn't one single "correct" way to use booleans. Let's take a look
at the many different ways you will see booleans represented in C programs.

> Here is a [PDF](https://www.dii.uchile.cl/~daespino/files/Iso_C_1999_definition.pdf)
> copy of the C99 standard, for reference below.

## Pre-C99

In older versions of C (and even in C programs today), people used `int` instead of
an actual boolean type. A boolean is essentially a one bit integer, so storing a boolean value in
an `int` isn't terrible, but it doesn't do a good job of explaining intent: For example,
returning `2` from a function that uses an `int` instead of a boolean means that if
you are checking for `1` explicitly (ie, the `true` case), your check will fail, despite `1` and `2` being
truthy.

Here are a few ways you might find `bool`/`true`/`false` being defined:

```c
#define bool int
// or
typedef int bool;

#define true 1
#define false 0
// or
enum { false, true };
```

If you are stuck with something like C89 or ANSI C, then you have no other option then to
define your own `bool` type. If you are using C99 and up, use the following method:

## C99

In C99, a boolean type was added, called `_Bool`. You can define boolean data types,
and all is well:

```c
_Bool isProgrammer = 0;
```

Note that we can't use `true` or `false`. We will get into that later.

Why did they name it `_Bool`, and not `bool`? The reason is that other programmers had
already defined their own `bool` types, like in the last section.
If the C committee decided to add the `bool` type globally, it could cause issues with people
who had already defined `bool` to be something else.

Also, the C99 standard states that:

> "All identifiers that begin with an underscore and either an uppercase letter or another
> underscore are always reserved for any use."
> 
> - **ISO/IEC 9899:1999 § 7.1.3**

With that in mind, it is possible for the C standard to add in new data types (and other identifiers)
using a reserved name. So long as a user isn't already using the reserved name, everything should just work.

To make our lives easier, C99 also made the `bool`/`true`/`false` keywords available
via the `stdbool.h` header:

```c
#include <stdbool.h>

bool isProgrammer = true;
```

Although it is somewhat annoying that you need to include a header just to have access to these,
it is better then the alternative (defining your own bool type).

## C++

Although not directly related to C, when you are dealing with header files which might be included in both
C and C++ code, it might be important to note a few things:

* `bool` is a built-in data type (no need to include anything)
* `_Bool` is only available if you include `stdbool.h` or `cstdbool`
* Different C versions might not support the `stdbool.h` header (pre C99)

## Fin

That's it! Although it is somewhat minor, this is something that you will see all over the place in
C code, and is something to be on the lookout for.
