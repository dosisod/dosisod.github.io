# Lost at C: Function Prototypes

What do you think the following C program produces?

```c
#include <stdio.h>

void f() {
    puts("here");
}

int main(void) {
    f();
    f(1);
    f(1, 2, 3);
}
```

Compiling and running with `gcc file.c && ./a.out`:

```
here
here
here
```

What is going on here?

## `f(void)` vs `f()`

In C++, `f(void)` and `f()` will do the same thing (in fact, using `f(void)` is
frowned upon in C++). In C though, there is a semantic difference: Since our
function `f` is a not a complete prototype, we are able to pass as many
arguments to it as we want.

This is normally not what you want, and can hide errors in your code. You can
enable the `-Wstrict-prototypes` flag in GCC/Clang to warn on incomplete
prototypes like the one we created above.

When declaring a function that doesn't take any parameters in C, you should use
`f(void)`, unless you have a good reason not to.

## More Prototype Fun

Another fun thing about C is that you can drop the names of your function parameters
in your function prototypes. For example:

```c
int add(int, int);

// define "add" elsewhere

int main(void) {
    return add(1, 2);
}
```

Since we don't define `add`, we won't be able to compile it, but that's fine.

Why would this be useful you might ask?

Suppose we have 2 files, `file.h` and `file.c`. The `.h` file will have our function
prototype, and our `.c` file will have the actual definition. In this instance, we
will be specifying the parameter name(s) in both the `.c` and the `.h` file. What happens
when we change one of the parameter names of our function definition in the `.c` file? Nothing.
Everything will compile just fine. But, the names in our function declaration (`.h` file) will not
match the ones in our function definition, which could be confusing. By dropping the
name in the header file, you don't have to rename things twice.

> Note: Having the parameter names in the headers is usually a good idea, especially
> if these are part of an API, or are user facing. Having functions that self document
> is hard when there are no names for the parameters.
