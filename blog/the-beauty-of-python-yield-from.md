# The Beauty of Python's "yield from"

While implementing the UI framework for [cal9000](https://github.com/dosisod/cal9000),
I came across a really nice way of handling events and state changes, bubbling them up
to the caller in a way that is easy to debug and test.

In short, using `yield` and `yield from` are awesome ways to build message
and event based systems, which is what we will be doing today!

## Immediate Mode UI's

Before we get started, we need to learn a little about immediate mode UI's.
An immediate mode UI declaratively defines how
a UI should be rendered, using the control flow (if statements, functions, etc)
to define whether code should be rendered, allow for rendering sub-elements, and
so on. Throughout this blog, we will be refactoring the below example into something
that is easy to read, write, and test.

```python
def render_input_box():
    return input("What is your name? ")


def render_page():
    print("This is some title")

    name = render_input_box()
    print(f"Hello {name}!")

    print("This is some content")

if __name__ == "__main__":
    render_page()
```

This will allow us to build out our UI, which is nice. There is (a few) issues with this:

* `input` makes it harder to test, as we need to ask the user for input.
* `print` makes it harder to test, as we don't have a way to grab what was printed to the screen.

> We can "patch" the `input` and `print` functions in order to do our testing, but in general,
> this just adds complexity to our tests. Patching should be used when you have no easy way to
> pull out these functions which have side-effect.

So how do we begin?

## Dependency Injection

First things first, we need to inject our keyboard (ie, `input()`), that way we
can test our code:

```diff
-def render_input_box():
-    return input("What is your name? ")
+def render_input_box(keyboard):
+    return keyboard("What is your name? ")


-def render_page():
+def render_page(keyboard):
     print("This is some title")

-    name = render_input_box()
+    name = render_input_box(keyboard)
     print(f"Hello {name}!")

     print("This is some content")


if __name__ == "__main__":
-    render_page()
+    render_page(input)
```

Now we can supply our own `input` method for our test, and use `input` in our production code!

But how do we pull out our `print` function calls? Sure, we could dependency inject our `print`
function as well, but we are going to do something a little different instead...

## Yield

The `yield` keyword in Python can be used to return a value from a function, without actually
returning from the function. For example:

```python
def get_names():
    yield "alice"
    yield "bob"
    yield "charlie"

names = get_names()
print(next(names))
print(next(names))
print(next(names))
```

This will result in:

```
alice
bob
charlie
```

Basically, `yield` gives us a way to nicely build a generator, which can be used to send
messages, create infinite sequences, lazy-load data from a database, and so on. There are
some issues with this code, and that is if we call `next(names)` again, we will get an
exception, since we have no more values left. What we could do instead is this:

```python
for name in names:
    print(name)
```

This will automatically stop iterating when we are all out of names. Pretty cool!

We can apply this to our UI like so:

```diff
 def render_page(keyboard):
-    print("This is some title")
+    yield "This is some title"

     name = render_input_box(keyboard)
-    print(f"Hello {name}!")
+    yield f"Hello {name}!"

-    print("This is some content")
+    yield "This is some content"


if __name__ == "__main__":
-    render_page(input)
+    for content in render_page(input):
+       print(content)
```

This allows us to send messages back back to the caller, and they can print them
for us. This way, we don't have to add in a keyboard, we just send the data back
that we want printed.

## Stepping It Up

What if we want to add a bit more code to the `render_input_box` method, maybe print
something using `yield`?

```diff
 def render_input_box(keyboard):
-    return keyboard("What is your name? ")
+    yield "please enter your name"
+    name = keyboard()
+    yield f"Hello {name}!"


 def render_page(keyboard):
     yield "This is some title"

-    name = render_input_box(keyboard)
-    yield f"Hello {name}"
+    for x in render_input_box(keyboard):
+        yield x
```

Now whenever something is yielded from our `render_input_box` function, we just `yield`
it again in our `render_page` function. This works, but it means we need to add 2 lines for
every nested page we want to render. Surely there is a better way to do this, right?

## Yield From

The solution to our problems, `yield from`:

```diff
-    for x in render_input_box(keyboard)
-        yield x
+    yield from render_input_box(keyboard)
```

Ta da! `yield from` basically allows us to bubble up the yielded values for a given function.
Whenever a value is yielded from anywhere in our application, the value is bubbled up to
the `print(content)` line, and then execution continues as normal.

The end result looks something like this:

```python
def render_input_box(keyboard):
    yield "please enter your name"
    name = keyboard()
    yield f"Hello {name}!"


def render_page(keyboard):
    yield "This is some title"

    yield from render_input_box(keyboard)

    yield "This is some content"


if __name__ == "__main__":
    for content in render_page(input):
       print(content)
```

## Fin

That's it! `yield from` is a cool feature I found out about just recently, and found it useful
enough to share with the world.
