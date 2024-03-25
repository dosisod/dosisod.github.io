# Lost at C: The static keyword

The `static` keyword in C is very powerful, and has many different uses, depending on the context you
use it in. Let's take a look at some examples:

## Static Functions

```c
#include <stdio.h>

static void static_func(void) {
  puts("hello from static");
}

void not_static_func(void) {
  puts("hello from not static");
}

int main(void) {
  static_func();
  not_static_func();
}
```

Compiling/running with `gcc file.c && ./a.out` we get the expected output:

```
hello from static
hello from not static
```

We can take a look at the symbols that are in the `a.out` binary using the command `nm a.out`:

```
000000000000039c r __abi_tag
0000000000004030 B __bss_start
0000000000004030 b completed.0
                 w __cxa_finalize@GLIBC_2.2.5
0000000000004020 D __data_start
0000000000004020 W data_start
0000000000001070 t deregister_tm_clones
00000000000010e0 t __do_global_dtors_aux
0000000000003df0 d __do_global_dtors_aux_fini_array_entry
0000000000004028 D __dso_handle
0000000000003df8 d _DYNAMIC
0000000000004030 D _edata
0000000000004038 B _end
000000000000117c T _fini
0000000000001130 t frame_dummy
0000000000003de8 d __frame_dummy_init_array_entry
0000000000002118 r __FRAME_END__
0000000000004000 d _GLOBAL_OFFSET_TABLE_
                 w __gmon_start__
000000000000202c r __GNU_EH_FRAME_HDR
0000000000001000 T _init
0000000000002000 R _IO_stdin_used
                 w _ITM_deregisterTMCloneTable
                 w _ITM_registerTMCloneTable
                 U __libc_start_main@GLIBC_2.34
0000000000001165 T main
000000000000114f T not_static_func
                 U puts@GLIBC_2.2.5
00000000000010a0 t register_tm_clones
0000000000001040 T _start
0000000000001139 t static_func
0000000000004030 D __TMC_END__
```

Slimming down to just the parts we care about:

```
0000000000001165 T main
000000000000114f T not_static_func
0000000000001139 t static_func
```

We can see `t` next to our static function, and `T` to our globally accessible functions.

What does that mean? Well, that basically means that we can only access this function from
inside our single compilation unit, in this case, the `a.out` binary. If this was an
shared object file (or DLL in Windows-speak) such as `libsomething.so`, we would not be
able to call our `static_func` function.

This is really good for encapsulation, closing off internals that we don't want people to get
their hands on.

## Static Data

We can also define "global" variables as static, which will make them local to the single
compilation unit they are defined in. As an added bonus, static variables are zero/NULL initialized,
so you don't have to give them an initial value!

```c
#include <stdio.h>

static int x;

int main(void) {
  printf("x = %i\n", x);
}
```

Compiling and running with `gcc file.c && ./a.out` we get the expected `x = 0` output.

## Static Variables in Functions

Similar to static variables defined at the module level, we can also define a static variable
at the function level. The static variable will still be statically initialized (zeroed out),
but will retain it's values across all invocations of the function.

What does that look like?

```c
#include <stdio.h>

void counter(void) {
  static int value;
  value++;

  printf("ran counter %i times\n", value);
}

int main(void) {
  counter();
  counter();
  counter();
}
```

Compiling and running:

```
ran counter 1 times
ran counter 2 times
ran counter 3 times
```

Here we have a variable called `value`, which is statically initialized to zero. Each time we
run the `counter` function, it increments `value`, and prints it out.

Why would you do this?

Perhaps you have a function which computes a result, and instead of returning it directly, you
return a pointer. Since you don't want to deal with `malloc()`, you can just return a pointer to
a statically declared variable. Since the static memory is always present, you will always be able to
read from it, and not have to worry about stack corruptions and such.

What you have to be careful about is using stale versions of static variables, since
they might be updated without you knowing, especially in a threaded environment (if you are using `static`
in a threaded environment, make sure the caller is aware of any potential side effects!).

Another purpose could be to store the result of a computation one time when the function is first
called, and then return the computed value after each successive call:

```c
#include <stdio.h>

unsigned fib(unsigned n) {
  if (n <= 2) return 1;
  n -= 2;

  unsigned first = 1;
  unsigned second = 1;

  while (n) {
    unsigned tmp = second;
    second += first;
    first = tmp;
    n--;
  }

  return second;
}

unsigned compute(void) {
  static unsigned value; // <-- The part we care about

  if (!value) {
    value = fib(10);
    puts("computing");
  }

  return value;
}

int main(void) {
  printf("result: %u\n", compute());
  printf("result: %u\n", compute());
  printf("result: %u\n", compute());
}
```

When we compile and run, we get:

```
computing
result: 55
result: 55
result: 55
```

## Fin

Hopefully you got something useful out of this! `static`, like most things in C,
can be very powerful if used correctly, or let you write some nasty code if done
incorrectly.
