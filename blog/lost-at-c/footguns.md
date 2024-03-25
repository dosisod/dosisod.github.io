# Lost at C: Footguns (not enabling flags)

What do the following C programs have in common?

```c
// program_1.c

int main(void) {
  return main();
}
```

```c
// program_2.c

int main(void) {
  return 0.1 + 0.2 == 0.3;
}
```

```c
// program_3.c

#include <stdlib.h>

int main(void) {
  int *ptr = malloc(-1);
  *ptr = 123;

  int i = *ptr;
  free(ptr);

  return i;
}
```

The answer? All of these programs either hang, have bugs, or crash. Why? Because of simple
mistakes, mistakes that can be caught by your compiler if you just turn on a couple of
flags.

> When I say flag I am referring to the command line flags you add when compiling your
> code from the command line, ie: `gcc file.c -flag -another-flag` and do on.

## program_1.c

Use `-Winfinite-recursion` (included in `-Wall`). It checks for infinite recursion,
thus warning us about our troublesome program.

## program_2.c

The expression `0.1 + 0.2 == 0.3` will always be false due to floating
point arithmetic [^1]. Turning on `-Wfloat-equal` will let you know whenever you are
trying to make an "unsafe" comparison with a floating point number [^2].

## program_3.c

`malloc` takes a `size_t`, which is `unsigned`, but we are passing
in a negative integer, which is `signed`. In this case, the C compiler will convert
the small negative number into a massive positive one [^3]. On most systems, when allocating
a large amount of data, `NULL` will be returned. If you don't check for `NULL`, you
will get a segfault if you try to read or write to that address. To fix this, you can
turn on `-Wconversion`, which will check for integer sign conversions [^4]. This will
require you to explicitly cast the resulting value to the correct type before passing
it to `malloc`.

## Flags You Should Always Enable

As we have seen, there are a lot of bugs which can be avoided simply by enabling
a few flags. With that in mind, here are a list of flags you should always enable:

* `-Wall`
* `-Wextra`
* `-pedantic`
* `-Wformat=2`

These first 3 flags will enable a bunch of other flags, which makes it easy to
find a bunch of bugs very quickly. `-Wformat=2` will enable strong bound
checking for format strings (`printf`, `scanf`, etc).

## Flags You Should Try To Enable

These flags should be added, since they will greatly improve your code quality,
but might bring a bunch more errors to light:

* `-Werror`
* `-Wshadow`
* `-Wswitch-default`
* `-Wunused`

`-Werror` will turn all warnings into errors, meaning that you will need to fix
them before the build succeeds. This is a great option to turn on once you have
fixed all the errors, but a pain if you have a bunch of errors to fix first.
`-Wshadow` will warn about variables which are shadowed (declared in a child
scope, but with the same name as a variable in a parent scope). `-Wswitch-default` will
tell you if you have an unhandled case in a switch statement, meaning you need to
add a `default` case (just to he explicit). `-Wunused` warns about dead code,
specifically functions which are never called.

## Flags That Would Make This Blog Too Long If I Added Them

There are a plethora of flags which you can enable, but that would be a lot of
ground to cover. If you want to see all of the compiler flags (that GCC supports),
click [here](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).

> GCC and Clang have very similar flags, but not all of them are the same:
> Some flags that work in Clang might not work in GCC, and vice versa. Sometimes
> one compiler will support a flag option (ie, `-Wformat-overflow=2`), but the another
> might not support the `2` option.

For an list of compiler options I use in one of my C projects, click
[here](https://github.com/dosisod/skull/blob/master/config.mk).

> I just covered some of the basic flags, but I didn't even cover some of the more
> advanced flags, like sanitizers (run time segfault checker, null pointer checker,
> and address checker (use after free, stack overflow, etc)) and more! Maybe next
> time...

## Fin

That's all! Using C with out flags is like driving without a seat belt. Compiler
warnings and flags are meant to keep you from doing things you (probably)
don't want to do.

---

[^1]: See [https://0.30000000000000004.com/](https://0.30000000000000004.com/).

[^2]: Greater then or less then comparisons are fine, since they cover a wide
range of values. It is just the equal-to comparisons which are the issue, since
these compare to exactly 1 value, which may or may not be the same as what you
imagine it might be.

[^3]: `(size_t)-1` == 18446744073709551615 bytes == 16 exabytes. You probably
don't have that much ram.

[^4]: Always check the output of `*alloc` functions. Even if you have plenty of
memory, you can quickly run out if you have a bug.
