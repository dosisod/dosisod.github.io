# The Process of Finding a Bug

I spent a lot of time tracking down and fixing this bug, and thought it would make a good blog as to how I went about
solving it, and the mistakes and insights I gathered along the way.

## What Started It All

Yesterday I was working on my programming language, [Skull](https://github.com/dosisod/skull). In hopes of speeding things
up, I decided to start reducing my dependence on a C compiler, since having to invoke `cc` for the final linking of our
means we have to call a whole other program, which is quite expensive. So how did I go about doing that?

Typically, C programs use `main` as their entrypoint, but in reality, `_start` is the true entrypoint, created for you by
the compiler. It does a bunch of nice things for you, like setting up the parameters for your `main` function, and so on.

So why would you want to change that? Well, suppose you have a programming language, and to allow for people to create their own
functions called `main`. By creating your own `_start` method, you don't have to worry about conflicts with users
who want to name their functions being called `main`, since we aren't going to use it.

> We could just change the entrypoint of our program, but that would only move the problem elsewhere. Since we want to
> eventually not even use a C compiler at all, doing this to solve our linker issue is just a band-aid fix.

So I wrote commit [5b022ce0](https://github.com/dosisod/skull/commit/5b022ce092baa4ddc12e26720291e7e344e221f4), and pushed
it up to GitHub. I got an email saying that my CI job failed, and so I went to look:

```
<SNIP>

Step 26/26 : RUN cd test/docs/c-integration && make
 ---> Running in 8c94c05bb0e6
skull hello.sk -- hello.c -no-pie
./hello
make: *** [Makefile:5: all] Segmentation fault (core dumped)
The command '/bin/sh -c cd test/docs/c-integration && make' returned a non-zero code: 2
```

## Oh No! A Segfault!

I assumed that I just hadn't properly tested it before I pushed it up, so I re-ran the `pre-commit` file on my local machine:

```shell
$ ./pre-commit

<SNIP>

../../../build/skull/skull hello.sk -- hello.c -no-pie
./hello
hello, world!
../../../build/skull/skull hello2.sk -c
cc .hello2.sk.o hello2.c -no-pie -o hello2
./hello2
hello, world 2!

<SNIP>
```

It passed! The next step is to build the same `Dockerfile` that the GitHub Actions workflow actually uses to do all of the
CI testing:

```shell
$ docker build -f .github/workflows/Dockerfile .

<SNIP>

Step 25/26 : RUN cc test/libskull.c -o skull-shim && ./skull-shim
 ---> Running in 78b487694f22
Skull v0.7.0-63-g5b022ce0
Removing intermediate container 78b487694f22
 ---> 6e444c728e70
Step 26/26 : RUN cd test/docs/c-integration && make
 ---> Running in 175ca8540f0d
skull hello.sk -- hello.c -no-pie
./hello
make: *** [Makefile:5: all] Segmentation fault (core dumped)
The command '/bin/sh -c cd test/docs/c-integration && make' returned a non-zero code: 2
```

## Investigate Further

So now that I am able to reproduce it on my machine, I need to figure out what is causing the segfault. The image
that was built before the failing step has an image ID of `6e444c728e70`, so if I spin up a container using that
image, I can drop into a shell and poke around:

```shell
$ sudo docker run --rm -it 6e444c728e70 bash

I have no name!@928fdd7f9083:/app$
```

> `--rm` will remove the container when we are done, since we don't want to use it again after we are done.
> `-it` can be remembered as "interactive terminal". Basically, it allows us to talk to the container over
> our terminal.

For sanity, make sure the build still fails:

```shell
I have no name!@928fdd7f9083:/app$ cd test/docs/c-integration/ && make
skull hello.sk -- hello.c -no-pie
./hello
make: *** [Makefile:5: all] Segmentation fault (core dumped)
```

Now let's start poking around.

For clarity (and to make things look nicer), I am going to change the
[bash prompt](https://www.gnu.org/software/bash/manual/html_node/Controlling-the-Prompt.html)
so that it is easier to tell
which commands are being ran in the container (`container $`), and which ones are running on my host machine
(just a `$`):

```shell
I have no name!@928fdd7f9083:/app$ echo $PS1
${debian_chroot:+($debian_chroot)}\\u@\\h:\\w\$
I have no name!@928fdd7f9083:/app$ PS1="container \$ "
container $
```

Much better!

First things first we check that the hashes of the compiled `hello` program in the Ubuntu docker
container match the ones on my Arch system:

> Note: You shouldn't expect compiled binaries to be the same across different machines, let alone different operating
> systems. Since this is a pretty trivial program, I had a suspicion that the files might be the same, or at the
> very least, very similar.

```shell
$ shasum ./test/docs/c-integration/hello
7e70e18a4136106a124b5dab27deff8e2b92122f  ./test/docs/c-integration/hello

container $ shasum test/docs/c-integration/hello
9cc04720933cba9328fd353f97b35dc8494e8dbd  test/docs/c-integration/hello
```

They don't match, which is somewhat expected. Let's see why they are so different by dumping the assembly
via `objdump`.

On the host machine:

```shell
$ objdump -c ./test/docs/c-integration/hello

<SNIP>

0000000000401050 <hello>:
  401050:       55                      push   %rbp
  401051:       48 89 e5                mov    %rsp,%rbp
  401054:       48 83 ec 10             sub    $0x10,%rsp
  401058:       48 89 7d f8             mov    %rdi,-0x8(%rbp)
  40105c:       48 8b 45 f8             mov    -0x8(%rbp),%rax
  401060:       48 89 c6                mov    %rax,%rsi
  401063:       48 8d 05 9c 0f 00 00    lea    0xf9c(%rip),%rax        # 402006 <_int_pow+0xf1e>
  40106a:       48 89 c7                mov    %rax,%rdi
  40106d:       b8 00 00 00 00          mov    $0x0,%eax
  401072:       e8 99 ff ff ff          call   401010 <printf@plt>
  401077:       90                      nop
  401078:       c9                      leave
  401079:       c3                      ret

<SNIP>
```

In the docker container:

```shell
container $ objdump -c ./test/docs/c-integration/hello

<SNIP>

0000000000401050 <hello>:
  401050:       f3 0f 1e fa             endbr64
  401054:       55                      push   %rbp
  401055:       48 89 e5                mov    %rsp,%rbp
  401058:       48 83 ec 10             sub    $0x10,%rsp
  40105c:       48 89 7d f8             mov    %rdi,-0x8(%rbp)
  401060:       48 8b 45 f8             mov    -0x8(%rbp),%rax
  401064:       48 89 c6                mov    %rax,%rsi
  401067:       48 8d 05 98 0f 00 00    lea    0xf98(%rip),%rax        # 402006 <_int_pow+0xf16>
  40106e:       48 89 c7                mov    %rax,%rdi
  401071:       b8 00 00 00 00          mov    $0x0,%eax
  401076:       e8 95 ff ff ff          call   401010 <printf@plt>
  40107b:       90                      nop
  40107c:       c9                      leave
  40107d:       c3                      ret

<SNIP>
```

Weird. The only difference between the two outputs is that there is this `endbr64` instruction that is
sprinkled in to the Ubuntu output. Let's look up what that means:

[From Stack Overflow](https://stackoverflow.com/a/56910435):

> It stands for "End Branch 64 bit" -- or more precisely, Terminate Indirect Branch in 64 bit.

Doesn't sound harmful. Other then that instruction, these binaries look almost identical.
What happens if we just copy over and run the working binary from the Arch system?

First we get the container id of our container (in another terminal):

```shell
$ sudo docker ps
CONTAINER ID   IMAGE          COMMAND   CREATED          STATUS          PORTS     NAMES
928fdd7f9083   6e444c728e70   "bash"    32 minutes ago   Up 32 minutes             naughty_cannon
```

Then we actually copy it:

```shell
$ sudo docker cp test/docs/c-integration/hello 928fdd7f9083:/tmp/hello
```

Then we check the hash (just to double check), and run it:

```shell
container $ shasum /tmp/hello
7e70e18a4136106a124b5dab27deff8e2b92122f  /tmp/hello

container $ /tmp/hello
Segmentation fault (core dumped)
```

Ok, so the binary is not the cause of the issue. It must be either Ubuntu, or the environment we created
after installing all of our dependencies, or both!

## MVP Time

Now that we have a good idea of what the root cause is, let's create the smallest possible environment
which will recreate the issue.

We will create a new folder somewhere, add a Dockerfile, and a simple C program:

```dockerfile
FROM ubuntu:22.04

RUN apt update && \
    apt upgrade && \
    apt install gcc-11 -y

WORKDIR /app
COPY file.c .

RUN gcc-11 -nostartfiles file.c
RUN ./a.out
```

Note that we are using Ubuntu Jammy (22.04). This will be important for later.

Add the following in our `file.c` file:

```c
#include <stdio.h>
#include <stdlib.h>

void _start(void) {
    puts("hello world");
    exit(0);
}
```

> For good measure, you should build this on your host machine first, and make sure
> that it runs as expected. You don't want to spend a bunch of time fixing the wrong error!

Now build the container, and see what happens!

```shell
$ sudo docker build .

Step 1/6 : FROM ubuntu:22.04
 ---> 3f4714ee068a
Step 2/6 : RUN apt update &&     apt upgrade &&     apt install gcc-11 -y
 ---> Running in af582fe738f5

<SNIP apt stuff>

Removing intermediate container af582fe738f5
 ---> 58eee8b4c01a
Step 3/6 : WORKDIR /app
 ---> Running in 777fc78a948d
Removing intermediate container 777fc78a948d
 ---> 10defe2ee273
Step 4/6 : COPY file.c .
 ---> 101465eeb7a0
Step 5/6 : RUN gcc-11 -nostartfiles file.c
 ---> Running in 9fca80a45234
Removing intermediate container 9fca80a45234
 ---> caa232378a47
Step 6/6 : RUN ./a.out
 ---> Running in eb7fd3b7f0ec
Segmentation fault (core dumped)
The command '/bin/sh -c ./a.out' returned a non-zero code: 139
```

Now that we have a smaller area to search, we can start digging deeper.

## Debugging Time

Perhaps we can install [`gdb`](https://sourceware.org/gdb/), and see if that can give us a better indication of what
is going on:

```diff
 RUN gcc-11 -nostartfiles file.c
+
+RUN apt install gdb -y
+RUN gdb ./a.out -q -ex r
 RUN ./a.out
```

When running `gdb` from the command line, we need to use the `-ex` flag to pass the commands we want to run,
since we won't be able to type them during the build. `-q` means quiet, which hides the banner when first starting.

Let's rebuild and see what happens:

```
Step 7/8 : RUN gdb ./a.out -q -ex r
 ---> Running in 31b33923158c
Reading symbols from ./a.out...
(No debugging symbols found in ./a.out)
Starting program: /app/a.out
warning: Error disabling address space randomization: Operation not permitted
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
4375    ./malloc/malloc.c: No such file or directory.

Program received signal SIGSEGV, Segmentation fault.
0x00007fa75da97540 in _int_malloc (av=av@entry=0x7fa75dc0cc80 <main_arena>, bytes=bytes@entry=640) at ./malloc/malloc.c:4375
(gdb) quit
A debugging session is active.

        Inferior 1 [process 16] will be killed.

Quit anyway? (y or n) [answered Y; input not from terminal]
```

Huh, we didn't call `_int_malloc`. What is going on here? Let's add `-ex bt` to our `gdb` command to print the backtrace,
and re-run:

```
Step 7/8 : RUN gdb ./a.out -q -ex r -ex bt
 ---> Running in 57cc66e861e1
Reading symbols from ./a.out...
(No debugging symbols found in ./a.out)
Starting program: /app/a.out
warning: Error disabling address space randomization: Operation not permitted
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
4375    ./malloc/malloc.c: No such file or directory.

Program received signal SIGSEGV, Segmentation fault.
0x00007f428808f540 in _int_malloc (av=av@entry=0x7f4288204c80 <main_arena>, bytes=bytes@entry=640) at ./malloc/malloc.c:4375
#0  0x00007f428808f540 in _int_malloc (
    av=av@entry=0x7f4288204c80 <main_arena>, bytes=bytes@entry=640)
    at ./malloc/malloc.c:4375
#1  0x00007f428808fa49 in tcache_init () at ./malloc/malloc.c:3245
#2  0x00007f428809025e in tcache_init () at ./malloc/malloc.c:3241
#3  __GI___libc_malloc (bytes=bytes@entry=4096) at ./malloc/malloc.c:3306
#4  0x00007f4288069c24 in __GI__IO_file_doallocate (
    fp=0x7f4288205780 <_IO_2_1_stdout_>) at ./libio/filedoalloc.c:101
#5  0x00007f4288078d60 in __GI__IO_doallocbuf (
    fp=fp@entry=0x7f4288205780 <_IO_2_1_stdout_>) at ./libio/libioP.h:947
#6  0x00007f4288077fe0 in _IO_new_file_overflow (
    f=0x7f4288205780 <_IO_2_1_stdout_>, ch=-1) at ./libio/fileops.c:744
#7  0x00007f4288076755 in _IO_new_file_xsputn (n=11, data=<optimized out>,
    f=<optimized out>) at ./libio/libioP.h:947
#8  _IO_new_file_xsputn (f=0x7f4288205780 <_IO_2_1_stdout_>,
    data=<optimized out>, n=11) at ./libio/fileops.c:1196
#9  0x00007f428806bf9c in __GI__IO_puts (str=0x5604a28d8000 "hello world")
    at ./libio/libioP.h:947
#10 0x00005604a28d7067 in _start ()
(gdb) quit
A debugging session is active.

        Inferior 1 [process 17] will be killed.

Quit anyway? (y or n) [answered Y; input not from terminal]
```

Huh! It seems to be hitting our `puts("hello world")` call, but after that, it just goes into neverland.
Let's install [`Valgrind`](https://valgrind.org/) and see what it has to say about our program. Valgrind
is typically used for finding memory leaks, illegal/undefined behavior, but it can also do a lot more.

Adding it is super easy:

```diff
 RUN gcc-11 -nostartfiles file.c

-RUN apt install gdb -y
-RUN gdb ./a.out -q -ex r -ex bt
-RUN ./a.out
+RUN apt install valgrind -y
+RUN valgrind ./a.out
```

Re-running:

```
Step 7/7 : RUN valgrind ./a.out
 ---> Running in 703095486b3a
==7== Memcheck, a memory error detector
==7== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==7== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==7== Command: ./a.out
==7==
hello world
==7==
==7== Process terminating with default action of signal 11 (SIGSEGV): dumping core
==7==  General Protection Fault
==7==    at 0x48F7F42: __pthread_once_slow (pthread_once.c:114)
==7==    by 0x49C6A52: __rpc_thread_variables (rpc_thread.c:59)
==7==    by 0x4A19D8C: free_mem (in /usr/lib/x86_64-linux-gnu/libc.so.6)
==7==    by 0x4A198C1: __libc_freeres (in /usr/lib/x86_64-linux-gnu/libc.so.6)
==7==    by 0x483F1B2: _vgnU_freeres (in /usr/libexec/valgrind/vgpreload_core-amd64-linux.so)
==7==    by 0x48A3551: __run_exit_handlers (exit.c:136)
==7==    by 0x48A360F: exit (exit.c:143)
==7==    by 0x109070: (below main) (in /app/a.out)
==7==
==7== HEAP SUMMARY:
==7==     in use at exit: 0 bytes in 0 blocks
==7==   total heap usage: 1 allocs, 1 frees, 4,096 bytes allocated
==7==
==7== All heap blocks were freed -- no leaks are possible
==7==
==7== For lists of detected and suppressed errors, rerun with: -s
==7== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```

This is even weirder! We seem to be getting our `hello world` printed, but then the program dies somewhere in
`exit`, which is different then what we where getting with gdb. Valgrind will swap out `malloc()` calls (among others)
with it's own version to be able to do it's memory analysis, which might explain this difference in behavior.

> The `==7==` output in Valgrind is to differentiate between our program's output, and Valgrind's output. The `7`
> means that our `hello` program is running under PID (process ID) 7.

Ok, this is all very weird. Our code is segfaulting in parts which are not in our control. It works just fine on
my Arch machine, but not in an Ubuntu 22.04 container. What if we downgrade to an older Ubuntu docker image, say 21.04 or 20.04?

```dockerfile
FROM ubuntu:21.04

RUN apt update && \
    apt upgrade && \
    apt install gcc-11 -y

WORKDIR /app
COPY file.c .

RUN gcc-11 -nostartfiles file.c

RUN ./a.out
```

Running:

```
Step 6/6 : RUN ./a.out
 ---> Running in 9931a6a2e7ee
hello world
```

Success! Well, not really. We still don't know what is causing this. And, we cannot downgrade too far, because we need
LLVM 13 in order to build Skull. The `llvm-13` package is only available in Ubuntu Impish (21.10) and up. Still, having code
that fails on the newest LTS version of Ubuntu is not good, and we should fix that problem instead.

## The Solution

Although anti-climatic, I found the solution in a [Stack Overflow comment](https://stackoverflow.com/questions/29694564/what-is-the-use-of-start-in-c)
after many insanity-questioning hours:

> Note that this `_start` is unsafe, violating the ABI when it calls `my_main`; you tell the compiler it's a
> normal function, but actually it's entered with the stack-pointer already aligned (e.g. on x86-64, RSP % 16 == 0),
> not RSP % 16 == 8 like on entry to a normal function after a `call` that pushes an 8-byte return address. You can
> fix that with `__attribute__((force_align_arg_pointer))` for `_start` to tell GCC that the stack pointer may be
> "misaligned" on entry to that one "function", as shown in [Get arg values with inline asm without Glibc?](https://stackoverflow.com/a/50283880/224132)

So, we set our Dockerfile back to version 22.04, and update our C file to the following:

```diff
-void _start(void) {
+void __attribute__((force_align_arg_pointer)) _start(void) {
```

And re-run:

```
Step 6/6 : RUN ./a.out
 ---> Running in d5407535deb7
hello world
```

Actual success! Now we just need to figure out what LLVM we need to change/add to make our compiler spit out proper code.

Up until now we have been using gcc for our compiler, but for any LLVM related shenanigans, we should use
[Clang](https://clang.llvm.org/). Since we have figured out what the issue is for the most part, we don't need to use
docker anymore, and can just run this on our local machine.

To figure out what we need to change, we will compile both the original (non-working) version and the new (working)
version of `file.c`, and compare the LLVM IR between the 2:

```
$ clang file-old.c -S -emit-llvm
$ clang file.c -S -emit-llvm
$ diff file-old.ll file.ll

20c20
< attributes #0 = { noinline nounwind optnone sspstrong uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
---
> attributes #0 = { noinline nounwind optnone sspstrong uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "stackrealign" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
```

Seems like the only thing that changed is the addition of the `"stackrealign"` attribute on the new one, so now we need to
just figure out how to add that attribute to our `_start` function and we should be set.

By the time I had figured out what the issue was, it was midnight, and I needed some sleep. After some well deserved rest,
I spent another 2-3 hours searching online, trying to find out how to add attributes to functions using the LLVM C API.
Eventually I found it, and here is the one line change in all of it's glory:

```diff
--- a/skull/codegen/llvm/write.c
+++ b/skull/codegen/llvm/write.c
@@ -348,6 +348,7 @@ static void add_start_shim(SkullStateLLVM *state) {
        );

        LLVMSetLinkage(start_func, LLVMExternalLinkage);
+       LLVMAddTargetDependentFunctionAttr(start_func, "stackrealign", "");

        LLVMTypeRef exit_func_type = type_to_llvm_func_type(
                &TYPE_VOID,
```

## Fin

That's it! A total of about 6 hours spent investigating a single segfault, which manifested itself on a single operating system
(that I could tell), and was solved with a single line of code. It goes without saying, but without a proper test suite,
I might not have found out about this bug for a very very long time!

There where a lot of dead ends, and major derails which I will not delve into, this blog is already long enough!
I hope this can teach someone about the debugging process, what things to look for, and how to stay sane when
debugging things which you have no idea how to.
