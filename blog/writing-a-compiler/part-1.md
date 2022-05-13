# Writing a Compiler (Part 1): Project Setup

At the end of this blog we will have setup a basic git repository with the following:

* Linting with [flake8](https://github.com/PyCQA/flake8), [isort](https://github.com/PyCQA/isort), and [black](https://github.com/psf/black)
* Testing with [pytest](https://github.com/pytest-dev/pytest) and [pytest-cov](https://github.com/pytest-dev/pytest-cov)
* Static type checking with [mypy](https://github.com/python/mypy)
* CI ([Continuous Integration](https://docs.github.com/en/actions/automating-builds-and-tests/about-continuous-integration)) with GitHub Actions

We will be starting from scratch so you can follow along yourself, but the code
is available [here](https://github.com/dosisod/write-a-compiler) for reference.

Let's jump in!

> In this blog (and all future blogs), I will be assuming that you are using
> Linux. If you are using Windows, you might be able to follow along, but some
> things might not work as expected. If you are using Windows, you can install
> [WSL](https://aka.ms/wsl) (Windows Subsystem for Linux), which will allow you
> to run most of these commands without any issues.

> I also assume you have a basic understanding of [git](https://git-scm.com/),
> or at the very least, a GitHub account, since we will be using GitHub
> Actions.

## Basic Folder Scaffolding

Start off by creating a new folder, and initializing a new git repo:

```
$ mkdir write-a-compiler
$ cd write-a-compiler
$ git init
```

Now we can start creating the basic folder structure of the project. This what
our folder structure will look like:

```
write-a-compiler
├─.github
│ └─workflows
├─test
└─wac
  ├─ast
  ├─codegen
  │ ├─python
  │ └─llvm
  ├─parse
  └─semantic
```

These are what each of the folders will (eventually) be doing:

* `write-a-compiler`: The root of our project
* `.github/workflows`: Holds our GitHub Actions workflows
* `test`: Where we will be writing all of our tests
* `wac`: The actual compiler source code. Short for "Write A Compiler"
* `wac/parse`: This is the "frontend", which will ingest/tokenize/AST-ify our code
* `wac/ast`: The interface between the parser, and semantic/codegen pipelines
* `wac/semantic`: Semantically analyze our AST nodes/trees
* `wac/codegen/python`: The code generator for compiling AST tree to python code
* `wac/codegen/llvm`: Same as the python one, but for LLVM

To create these folders, run the following:

```
$ mkdir -p .github/workflows test wac/{ast,codegen/python,codegen/llvm,parse,semantic}
```

The `-p` flag of `mkdir` will allow for the creation of nested folders without
needing to create the parent folder first. The `{}` brackets will cause all the
comma separated values to be expanded, with the values to the left/right of the
brackets prepended/appended (if they exist) for each of the comma separated values.
For example, `a{a,b}c` will be expanded to `aac abc`.

## Adding a License

Before we start writing any code, we should license our software so people
know whether they can modify our software or not, and if so, what sort of
rules and limitations they need to abide by. The
[write-a-compiler](https://github.com/dosisod/write-a-compiler) codebase
that this blog is based off of uses the
[GPLv3 license](https://www.gnu.org/licenses/gpl-3.0.en.html), and I would
recommend that you use it for yours, just because the resulting codebases will
look very similar, and re-licensing under a different license could be
problematic.

To add the license, download the GPLv3 license from the GNU website, and pipe it to
a file called `LICENSE`:

```
$ curl https://www.gnu.org/licenses/gpl-3.0.txt > LICENSE
```

## Adding the Dependencies

### Creating the Virtual Environment

Before we do anything else, we need to install our Python packages. Before we
do that though, we will need to setup a
[virtual environment](https://pythonbasics.org/virtualenv/).
This will basically allow us to create a little bubble for our Python project,
so that we don't have to install our packages globally. Globally installed
packages are harder to work with in general, especially when it comes to
versioning. We can setup a virtual environment with the following:

```
$ python3 -m virtualenv .venv
```

> If `python3` doesn't exist, you might need to use something like `python3.9`
> instead.

Then, we need to activate the virtual environment:

```
$ source .venv/bin/activate

# your prompt will be updated to look something similar to below
(.venv) $
```

> Note: you will need to reactivate the virtual environment every time you
> open a new terminal window. Exit a virtual environment without closing the
> terminal window by running `deactivate`.

### Installing the Packages

Now we can actually install our packages!

```
$ pip3 install mypy black flake8 pytest pytest-cov isort
```

To make sure that we always get the same package versions every time someone
clones our code from GitHub, we will "freeze" our packages. This will take a
snapshot of all of our installed packages and their versions:

```
$ pip3 freeze > dev-requirements.txt
```

The little `>` symbol tells our shell to redirect the output of `pip3 freeze`
into the file called `dev-requirements.txt` (try running just `pip3 freeze` and
see what happens).

We will also create an empty `requirements.txt` file, which will store the
dependencies for our actual production code, which doesn't exist yet:

```
$ touch requirements.txt
```

### Configuring the Linters

These configurations are subject to change, and can be changed based on your
personal preference, though I have found these to be pretty sane defaults.
Basically just copy and paste these into their respective files:

Flake8 (file goes in `.flake8`):

```ini
[flake8]
exclude = .git,__pycache__,.venv
```

Mypy (file goes in `.mypy.ini`):

```ini
[mypy]
check_untyped_defs=True
disallow_any_decorated=True
disallow_any_explicit=True
disallow_any_generics=True
disallow_any_unimported=True
disallow_incomplete_defs=True
disallow_subclassing_any=True
namespace_packages=True
no_implicit_optional=True
strict_equality=True
warn_redundant_casts=True
warn_return_any=True
warn_unreachable=True
warn_unused_configs=True
warn_unused_ignores=True
```

There are some files I didn't bother to fully setup yet, since there is no real
code to run these programs against yet. This should be good enough for now.

Now we can run `flake8` (for example), and flake8 will lint our code for us.

## Make-ing Things Easier

We just added a bunch of programs, and they all do different things: Mypy checks
types, Flake8/Black standardize the format our code, and so on. Having to run
these commands manually will be a pain. And if there are parameters we need to pass
to these programs from the command line, we won't want to have to type those
out all by hand each time.

To make our lives easier, we can use Makefiles, which will allow us to run
"recipes" when a "target" needs to be built. Here is the contents of our `Makefile`:

```makefile
test: flake8 mypy black isort pytest

flake8:
	flake8

mypy:
	mypy -p wac
	mypy -p test

black:
	black wac test -l 79 --check --diff --color

isort:
	isort . --diff

pytest:
	pytest test --cov --cov-report=html
```

Now we can simply type `make test` to run `flake8`, `mypy`, etc., or `make pytest`
to run just pytest.

## Adding CI

As we make changes to our codebase in the future, we will need to ensure that
the quality of the code is as high as possible, and has as few bugs as possible.
To do this, we use Continuous Integration (CI), which will make sure that all new
code introduced into the codebase is high quality. Here is the workflow we will be
using:

`.github/workflows/actions.yml`:

```yml
name: tests

on: [push, pull_request]

jobs:
  tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Pip install
        run: |
          pip install -r requirements.txt
          pip install -r dev-requirements.txt

      - name: Run flake8
        run: make flake8

      - name: Run mypy
        run: make mypy

      - name: Run black
        run: make black

      - name: Run isort
        run: make isort

      - name: Run pytest
        run: make pytest
```

The `on` field specifies a list of
[events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)
which will trigger our workflow. In this case, whenever a PR (pull request)
is made, or code is pushed to a branch (on GitHub), our workflow will run.

The `jobs` field specifies only one job, `tests`. `tests` will run on an Ubuntu
docker container (as specified by the `ubuntu-latest` value of `runs-on`). Each
`step` is a list of instructions to run. If any one step fails, the whole
workflow fails, indicating of the code we tried to merge in did not pass one of
our tests.

This `actions.yml` file could be named anything, since GitHub will check the
`.github/workflows` folder for any `.yml` files, and run what it needs based
on the contents of the file.

## Making Git Happy

### Ignoring Certain Files/Folders

There are a lot of files which we don't want to have in our git repository,
such as the `.venv` folder and such. Here is what I have in my `.gitignore`
file currently:

```
.venv
__pycache__
.mypy_cache
.pytest_cache
.coverage
```

This should prevent us from accidentally committing junk files into our nice
clean codebase!

### Add Missing Folders

If we run `git status`, we won't see any of our folders, because git doesn't
track folders, it tracks files. To get around this, we need to add placeholder
files in the directories we want to keep:

```
$ touch wac/{ast,codegen/python,codegen/llvm,parse,semantic}/__init__.py
```

This will put a filename called `__init__.py` into each of these folders
that we care about.

### Add "pre-commit" File

A `pre-commit` file is a file which will be ran before each commit is made.
This is somewhat like our CI workflow, but it is meant for our local development
environment instead. If the `pre-commit` fails, the commit will be aborted.

For security purposes, the `pre-commit` file is not ran by default: we need to add
it to a special folder before git will run it. The folder in question is
`.git/hooks`. If we take a look inside it:

```
$ ls -1 .git/hooks
applypatch-msg.sample
commit-msg.sample
fsmonitor-watchman.sample
post-update.sample
pre-applypatch.sample
pre-commit.sample
pre-merge-commit.sample
prepare-commit-msg.sample
pre-push.sample
pre-rebase.sample
pre-receive.sample
push-to-checkout.sample
update.sample
```

You can see we have a bunch of `.sample` files, which are just placeholders.
We need to make a `pre-commit` file to our local folder, and then symlink
it to a file called `.git/hooks/pre-commit`.

> A symlink is a file which is "linked" or "references" another file.

We will create a basic pre-commit file, and symlink it to our hooks folder:

`pre-commit`:

```
#!/bin/sh

make test
```

The `#!/bin/sh` line is a [shebang](https://en.wikipedia.org/wiki/Shebang_&#40Unix&#41).
It tells the shell which program it should use to run our script. In this case,
we are telling it to use `/bin/sh`.

We can now symlink it with:

```
$ ln -sf $PWD/pre-commit .git/hooks/pre-commit
```

Now whenever we want to make a commit, our `pre-commit` file will run, and if we
update our `pre-commit` file, we won't need to copy/re-symlink it again!

If we want to run our `pre-commit` file directly, we need to make the file executable:

```
$ chmod +x pre-commit
```

`chmod` (aka "change mode") allows us to change the file attributes of a file.
`+x` will add the executable flag to our `pre-commit` file. Now we can just run
our pre commit file using `./pre-commit`.

## Adding a Test

Now that we have the basic folder structure setup, we can start writing a
test to make sure we have all of our dependencies setup correctly. We can
add the following to `test/test_placeholder.py`:

```python
def test_something():
    pass
```

Now if we run `make pytest`, we should see something like this:

```
pytest test --cov --cov-report=html
============================= test session starts ==============================
platform linux -- Python 3.10.2, pytest-7.1.1, pluggy-1.0.0
rootdir: /home/loot/git/write-a-compiler
plugins: cov-3.0.0
collected 1 item

test/test_placeholder.py .                                               [100%]

---------- coverage: platform linux, python 3.10.2-final-0 -----------
Coverage HTML written to dir htmlcov


============================== 1 passed in 0.03s ===============================
```

Our single `test_something` test passes! As we continue writing our compiler,
we will add more meaningful tests that make sure everything is working as expected.

## Add a README

A README file is for users and developers to get an overview of a project.
You can copy the version used in the reference repo
[here](https://github.com/dosisod/write-a-compiler/blob/master/README.md).

## Fin

We are done! Now all we need to do is push it up to our git repository:

```
$ git remote add origin git@github.com:USERNAME/REPONAME
$ git add .
$ git commit -m "Initial commit"
$ git push origin master
```

> Note: if you use the `git@github.com` syntax (aka SSH syntax), you will
> need to setup an SSH key with your GitHub account. You can see how to do
> that [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).
> Alternatively, you can use `https://github.com/USER/REPO`, and put in your
> username+password there.

## What's Next

Now that we have everything setup, we can start working on the actual compiler!
More specifically, we will be working on the tokenizer, the first stage of any
compiler frontend.

[[prev](./writing-a-compiler-0.html)]
[[next](./writing-a-compiler-2.html)]
