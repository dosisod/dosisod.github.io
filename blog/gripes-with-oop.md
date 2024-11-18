# Gripes with OOP

I use OO languages all the time, but find there are a common string of annoyances
I have with them. Some of these are inherit to OOP itself, some of them how certain
OO features are implemented in a certain language, and others are how OOP is used
in a general sense.

## Class Dogma

Some languages are multi-paradigm (C++, Python, etc), but some are strictly OOP [^1].
What happens if you want a function in Java that adds 2 numbers? Sorry, that needs
to go into a class.

Certain things don't (always) need to go in a class:

* Pure functions
* Constants
* Static class methods

Pure functions have no side effects, and as long as they are properly named, shouldn't
need to be tied to a class in any way.

Constants cannot change, and as such, should be able to be defined anywhere you please,
so long as it makes sense.

Static classes are purely designed to hold static methods and nothing else. In C++/C#,
a namespace could be used to group like things together, instead of a static class.
They do the same thing, but one of them doesn't need to create a class to do so (even if
it is just a single class). Take for instance the [Java Math library](https://docs.oracle.com/javase/8/docs/api/java/lang/Math.html),
which is just a bunch of functions wrapped up in a static class called `Math`.

## Scope and Readability

As someone who doesn't (normally) use an IDE, it is annoying to see a variable, lets call
it `x`, and have no idea where it is defined:

```c++
// c++

void SomeClass::someMethod() {
  x++;
}
```

Is it some global variable? Is it defined
somewhere in this file? Is it a member of this class? Perhaps it is a member of the superclass?

Without an IDE to tell you, you might never know. Even with an IDE, sometimes your IDE is slow, and
doesn't tell you right a way, and now you are waiting for it to finish scanning/running amok/whatever
else it is doing so that you can get on with your life.

Python uses `self.x` and `cls.x` for accessing instance and static data respectively, and this
makes it very easy to tell when something is part of a class or not. C++ has `this->x` and C#/Java
have `this.x`, and so on. But, these are usually frowned upon, and IDE's will tend
to gray them out, since they are "unnecessary" (in the case of C++/C#/Java).

## Getters/Setters

It is a "best practice" in Java to add getters and setters for all of your field methods,
since you never know when you might want to add more functionality to them:

```java
class SomeClass {
  public String name;
  public int age;

  // ...

  public String getName() {
    return name;
  }

  public int getAge() {
    return age;
  }

  public void setName(String n) {
    name = n;
  }

  public void setAge(int n) {
    age = n;
  }
}
```

There are 3 lines that are important, and that is:

1. The name of the class
2. The `name` field
3. The `age` field

There is also the constructor, which I left out.

This dogmatic approach to writing code takes away from the things that matter, which is certainly not
the silly getter/setters. There is this Java library called [Lombok](https://projectlombok.org/),
and adds a lot of attributes for auto-generating getters/setters, making builder classes, and so on.

In Python, we have dataclasses, which further reduces the class boilerplate:

```python
from dataclass import dataclass

@dataclass
class SomeClass:
    name: str
    age: int

x = SomeClass(name="bob", age=123)
x.name = "alice"
```

Python and C# have the idea of getter/setter properties, which allow for calling a function
when assigning/reading from a field. This means that you can "add" a getter/setter after
the fact, and not have to write any boilerplate functions!

## Encapsulation

Gasp! Encapsulation is good, but there are times where you need to break the rules, and your
language makes it hard to do so. For example, in Python, everything is public, there isn't any
way of locking things down [^2]. This sounds heretical to non-Python programmers, but
once you get used to it, it is actually really nice.

C++, C#, and Java have the concept of `friend`/`protected` members, which allow for code
inside the same "module" to get direct access (as if it where `public`), though restrict this
access to `private` outside the module. This can be good when you just need access to something
"this one time", or want to change something that the original authors (perhaps yourself) didn't
want you to.

## Lack of Understanding of OOP Concepts

This is more targeted at people who use OOP, or more specifically, don't use OOP for what it is
capable of. Ask yourself the following: When was the last time you:

* Wrote a destructor
* Wrote an abstract class
* Wrote a class that didn't extend some library interface of sorts

If you haven't done any of those recently, perhaps you aren't using OOP, just putting your code in
the right place so that it compiles and runs in whatever framework you chose.
OOP is, among other things, a way for you to manage the lifetime of objects, to keep relevant
functionality together, for creating hierarchies, for creating boundaries using interfaces and/or
abstract classes.

## Fin

That's all for now. I feel like I missed a few points, but all in all, this covers pretty much
everything important.

---

[^1]: Some previously strictly OOP languages (like Java/C#) are adopting more functional approaches,
and as such, might not be considered "strictly" OOP in the traditional sense.

[^2]: There are frozen classes and such, but they more or less just make it harder, not impossible.
