# Writing a Compiler: Before You Start

> Note: I assume that you have a basic understanding of programming languages,
> how they work, and how to do all of the basics (functions, control flow,
> building/running programs, etc). It doesn't matter which language, just so
> long as you have a basic grasp.

There are a lot of reasons why you might want to write your own compiler:

* You want to make your own programming language
* You want to port an existing language to a new platform
* You want to learn the magic that goes into creating/running your code or executables

All of these are good goals and aspirations. A few things to keep in mind though:

* The larger the project, the longer it will take to complete
* The more complex the language, the more complex the compiler
* The less planning ahead you do, the more scurrying around you will do

Writing a compiler is very rewarding, and can be very fun. Just know that, like
with any project, knowing what it is that you are getting yourself into is very
important, and makes sure you don't loose sight of the end goal.

If you decide to make your own programming language, understand that not only
are you writing a compiler, but you are also designing a language: You need to
figure out the syntax, the structure, how it is all going to "fit together".

## What is a Compiler?

Basically, a compiler is something that takes in data (code, files, user input,
etc), manipulates it, and spits out some sort of result (binary/executable, an
image, code, etc). All compilers are written differently, as they do
different things, have different requirements and goals, and are built by
different people.

Compilers come in all sorts of shapes and sizes. Here are some examples:

**[GCC](https://gcc.gnu.org/)/[Clang](https://clang.llvm.org/)**:
These are very big compilers, capable of compiling many different
programming languages, primarily C and C++.
They are very mature, and do a lot of the heavy lifting for you in terms
of platform and hardware support, optimizations, and performance.

**[esbuild](https://esbuild.github.io/)**:
Esbuild is "an extremely fast JavaScript bundler", as stated on
their website. Basically, it takes in JavaScript, and spits out JavaScript.
This is an example of a source-to-source compiler, since it takes in, and
spits out source code.

**[My blog site](https://github.com/dosisod/dosisod.github.io)**:
All of my blogs are written in markdown, and converted to
HTML, which allows for easily writing blogs without the hassle of writing
the HTML myself (or having to change a bunch of HTML when I want to have
a different layout).

With all that being said, most compilers are split up into different chunks,
which we will see below.

## Parts of a Compiler

### The Front End

This is the part of the compiler that you will interact with most often.
It is responsible for taking in the code you give it, parsing it, and sending
it off to the next stages of the compiler. To make things easier, the data
from the file is parsed into a tree-like structure called an AST (abstract
syntax tree). Most compiler front ends do these steps:

* **Tokenization**: Split code into little "tokens", for example, each word or operator
* **Classification**: Each token is assigned a type based on it's contents
* **AST Generation**: The tokens are grouped up into meaningful "nodes", which represent different parts of the program (eg, a variable definition or function call)

### The Middle End

This is where the AST is checked for symantic errors, type checking is done,
and optionally, optimization(s) are performed. This is where the
"juicy" parts of most compilers live. The job of the middle end is to make sure
that the parsed code is valid, and to make sure that the optimizations are done
such that the backend don't have to worry about it.

### The Back End

After the AST has been checked, the backend will start to generate the
executable (or code). There are many techniques that a backend can use to
generate these files, which we won't get into right now. Some might compilers
only have one backend, while others might support many different backends.
This all depends on the wants and needs of the language designer.

## The Next Steps

At the end of this series, we will have created a simple programming language
in Python, which supports 2 backends: a Python backend, and an [LLVM](https://llvm.org/)
backend, which allows for building executables, and JIT compilation of our code.
