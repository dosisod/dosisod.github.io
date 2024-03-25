# Programming Language Review: Visual Basic

I have been using Visual Basic (VB) at work a lot, and I have some (many) opinions about it. Having
[created a programming language](https://github.com/dosisod/skull) myself, I find the design decisions and
little features/quirks of this language very fascinating.

I read through (most) of the [Visual Basic docs](https://docs.microsoft.com/en-us/dotnet/visual-basic/language-reference/)
on MSDN before I started seriously looking
at any VB code, and I am glad I did! There are a lot of weird "features" which aren't present in
most other languages, and other things that just don't make any sense. VB shares a pretty good feature parity
between C# (VB, C#, and F# the 3 main languages that make up the .NET family of
languages), despite Microsoft [halting future development on VB](https://devblogs.microsoft.com/vbteam/visual-basic-support-planned-for-net-5-0/).

Saving the best for last, let's dive into some VB code!

## Unforgivable

There are some things that VB does which are just plain wrong:

```vb
' Using single quotes as a comment. Makes grep'ing for things harder
' Also, no multi-line comments

' Why in the world would you use <> for the "not equal" operator?
Dim isNameNotBob As Boolean = name <> "bob"

Dim str As String = "using ampersands " & "for" & " string concatenation"
```

These are just minor annoyances, but can be overlooked. They just don't make sense, that's all.
But, there are some things which just sinful:

### It's Case Insensitive

Yep. It is really jarring to see the same variable with different cases. It just brings a certain
feeling of uncertainty when working on a project.

Depending on your IDE (Visual Studio 2022, I am looking at you), it might also just go ahead and
"normalize" your symbols for you, changing the casing to the casing of the original variable. In our
codebase, we ~~have~~ had a global variable called `sql`, and in doing refactorings, Visual Studio would rename `sql`
to `Sql` (note the capital `S`), since `Sql` was a namespace which we had available. When you added in the
local `sql` variable back in, it wouldn't change it back for you! You would end up with code like this:

```vb
Dim sql = "SELECT * FROM table_name"

run(Sql)
```

I get that the keywords in Visual Basic are case-insensitive, and that is fine, but identifiers? That
is too far IMO.

> Note that Visual Studio has nothing to do with the VB language itself, but it does do a good job of accentuating
> this particular design flaw in VB.

### Implicit Function Calls

Another fun fact about VB is that [functions that don't take arguments can be called without using any
parenthesis](https://docs.microsoft.com/en-us/dotnet/visual-basic/language-reference/statements/function-statement#calling-a-function):

```vb
Function f() As Integer
    Return 1337
End Function

Sub Main()
    Console.WriteLine(f)
End Sub
```

I don't know why this is the case. Even the docs say not do do it.

### Type Conversion Suffixes

Given the following example:

```vb
Dim a = "1234"
Dim b$ = "1234"
Dim c# = "1234"
Dim d% = "1234"
Dim e! = "1234"
Dim f@ = "1234"
Dim g& = "1234"

Console.WriteLine(a & " " & TypeName(a))
Console.WriteLine(b & " " & TypeName(b))
Console.WriteLine(c & " " & TypeName(c))
Console.WriteLine(d & " " & TypeName(d))
Console.WriteLine(e & " " & TypeName(e))
Console.WriteLine(f & " " & TypeName(f))
Console.WriteLine(g & " " & TypeName(g))
```

What do you expect this code to return?

```
1234 String
1234 String
1234 Double
1234 Integer
1234 Single
1234 Decimal
1234 Long
```

What is going on here? Well, ["type characters"](https://docs.microsoft.com/en-us/dotnet/visual-basic/programming-guide/language-features/data-types/type-characters)
of course! They are these little warts you can sprinkle on your code which let you declare the type of the variable using the name of
the variable itself. Not fun.

You can also cast the result of a function just as easily using these same conversion symbols:

```vb
Dim name = "Billy Bob"

Console.WriteLine(Left$(name, 5))
```

This will print `Billy` (as a string), since `$` is the type character for string conversions.

> `Left` already returns a string, so the `$` is redundant, but you get the point.

## Unfortunate

These next few things are interesting "features", gotchas, or both! They aren't as egregious
as the last section, but they might trip you up if you aren't paying attention.

### Short Circuiting

And I'm not talking about that one [Daft Punk Song](https://youtu.be/9hhVnRTNVmM).

You might not know what short circuiting is off the top of your head, but you have definitely experienced it at some point.
Take the following Python code for example:

```python
def proxy(x):
    print(f"proxy: {x}")
    return x

def expensive():
    print("some expensive call")
    return true

a = proxy(False) and expensive()
b = proxy(True) and expensive()
```

When running, we get:

```
proxy: False
proxy: True
some expensive call
```

As you can see, our `expensive` function is only called if the `proxy` method returns true. If it returns false
(like in the first example), it doesn't matter what `expensive` returns, the expression will always evaluate to
false. This is really nice if you only want to call something expensive if a certain condition is met, or want to
reduce the number of unnecessary computations in your program.

So, what happens in VB you might ask?

```vb
Function proxy(x As Boolean) As Boolean
    Console.WriteLine("proxy: " & x)
    return x
End Function

Function expensive() As Boolean
    Console.WriteLine("some expensive call")
End Function

Sub Main()
    Dim a = proxy(false) And expensive()
    Dim b = proxy(true) And expensive()
End Sub
```

Running:

```
proxy: False
some expensive call
proxy: True
some expensive call
```

So, one might think that VB doesn't have short circuiting, but they would be incorrect! VB does
indeed have support for short-circuiting, but you need to use a different operator, `AndAlso`!

> There is also an short-circuiting version of the `Or` operator called `OrElse`.

Changing our code to the following, we get the result we expected:

```vb
Sub Main()
    Dim a = proxy(false) AndAlso expensive()
    Dim b = proxy(true) AndAlso expensive()
End Sub
```

Running:

```
proxy: False
proxy: True
some expensive call
```

Why `AndAlso` isn't the default behavior, the world may never know. This might be due to with some BASIC backwards
compatibility issues, but who knows.

### Modules

Modularity is normally a good thing: it keeps our code in little compartments, and allows us to better organize our code.
Not in VB. A `Module` in VB translates to: "make the code in this block available, ***without the need for an `Import`***,
to all VB files in this project".

If you are looking for actual "modularity", use namespaces instead.

Modules (in VB) are really helpful for utilities which need to be available everywhere in the application, but can very
easily clog up the global namespace.

### Named Return Values

I really like named return values, and I think Golang does a good job of implementing it:

```go
func add(a int, b int) (sum int) {
    sum += a
    sum += b
    return
}

func main() {
    fmt.Println(add(1, 2))
}
```

This basically will add `a` and `b` together, storing the result in `sum`. When the function returns,
`sum` is returned automatically. Very nice!

VB on the other hand, does not do this nicely:

```vb
Function Add(a As Integer, b As Integer) As Integer
    Add += a
    Add += b
End Function

Sub Main()
    Console.WriteLine(Add(1, 2))
End Sub
```

What I really don't like is the fact that the return value is the same as the function name itself.
When you first see this, it might be confusing: Why are we assigning to the name of the function? Does
that even work?

Although the feature is "nice", it will be annoying when it comes time to rename that function (and VS 2022
won't rename the `Add` references if you change the function name).

### No New Expressions

Normally in C#, you can write this:

```csharp
public class SomeClass {
    public int SomeMethod() {
        Console.WriteLine("hello world");
        return 1234;
    }
}

static void Main() {
    int value = new SomeClass().SomeMethod(); // this line
}
```

Here we create a new instance of `SomeClass`, call its `SomeMethod`, assigning the result to `value`, and
destroying our temporary class instance.

In VB though, there is no good way of doing this:

```vb
' This line won't compile:
Dim value = New SomeClass().SomeMethod()

' Or this:
Dim value = (New SomeClass()).SomeMethod()

' This is the typical way you would do this (requires temp variable)
Dim temp As New SomeClass()
Dim value = temp.SomeMethod()
```

The closest you can get is using the [`Call` statement](https://docs.microsoft.com/en-us/dotnet/visual-basic/language-reference/statements/call-statement),
which allows for calling expressions which don't start with an identifier (ie, `New`). The only issue with `Call` is that it treats
the function/sub-procedure as a sub-procedure, discarding the result in the case of a function!

This seems to be a bug in the expression parser. There is no reason why you can assign the expression `New Something()` to a variable, but not use
that same expression to call a method on said expression (like `New Something().Method()`).

It is also unfortunate that you need a temporary variable because the lifetime of this variable now is extended to the end of it's bounding scope,
which could potentially the end of the function. In the case of C#, having the temporary instance allows for the garbage collector to free up resources
sooner, whereas VB has to wait until the scope is exited.

## Underrated

There are some things that I think makes VB really shine, things that more languages should pick up on.

### The Power Operator

Most languages use `**`, or a separate `pow` function to raise things to a power. This is how you do it in VB:

```vb
Dim square = 3 ^ 2
```

Beautiful.

Even though Python has the `and`, `not` and `or` keywords, it doesn't have `xor`, meaning it is stuck with `^` for
the xor operator, along with all the other C-style languages.

> See [this blog post](https://eev.ee/blog/2016/12/01/lets-stop-copying-c/) for more comparisons of C to other languages.

### Using Blocks

Like Python (and C#), VB has a `using` block for managing resources:

```vb
Using resource As New SomeResource
    ' use resource
End Using
```

Assuming that the `SomeResource` class implements the
[`IDisposable`](https://docs.microsoft.com/en-us/dotnet/api/system.idisposable?view=net-6.0)
interface, it can be used in a `using` block no problem. This is a really nice
pattern in Python, and makes cleaning up resources super easy.

### Events

One of the best features of VB that actually really surprised me is that it has built-in supports for events.
Basically, you attach `Handles SomeEvent` to the end of your sub-procedure, and it gets called whenever that
event is fired!

```vb
Public Class UserRepo
    Public Event UserRegistered(ByVal name As String)

    Public Sub Add(username As String)
        RaiseEvent UserRegistered(username)
    End Sub
End Class

Module VBModule
    WithEvents repo As New UserRepo

    Sub AddUserToDataBase(name As String) Handles repo.UserRegistered
        Console.WriteLine($"Adding user {name} to database")
    End Sub

    Sub SendWelcomeEmail(name As String) Handles repo.UserRegistered
        Console.WriteLine($"Sending Welcome email to {name}")
    End Sub

    Sub Main()
        repo.Add("Alice")
        repo.Add("Bob")
        repo.Add("Charlie")
    End Sub
End Module
```

> ~~Note that this code is untested. All of these VB examples were checked using
> online VB compilers, which uses [Mono](https://www.mono-project.com/docs/about-mono/languages/visualbasic/),
> Which has lacking support for certain VB features.~~

> Update: I found this cool site called [Coding Rooms](https://www.codingrooms.com/), which is an online
> IDE which supports live code-sharing, and so on. You can run this demo [here](https://app.codingrooms.com/w/5v3GRGdtCVsj).

This is really nice, because it allows for the caller and the callee to not interact with one another.
You just register the event you want to listen to, and when it is fired, your function gets called!

## Fin

That's it! There are probably some things I am missing, but this pretty much covers most of the "features" which
you will run into on a daily basis.

When I started really learning VB, I tried my best to remain neutral, to not love it or hate it, to look for the
good and the bad before I made my decision. I have made my decision. It could be better! It does a lot of things
right, but a lot of things are just not that great.
