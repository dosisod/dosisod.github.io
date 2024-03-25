# I Don't Like Ligatures

The title says it all. And just so we are on the same page, I am talking specifically
about ligatures used for programming, like the one below:

<img src="https://cdn-images-1.medium.com/max/1200/1*wP6e1QtYkm5ezm8QLA8wkA.gif" />

[Photo Credit](https://medium.com/larsenwork-andreas-larsen/ligatures-coding-fonts-5375ab47ef8e)

## They Can Change Font Width

Ligatures are basically just groups of characters that when together, display a
different character [^1]. This means that you can change the width of the
conjoined characters. For example, you could have a ligature font which changes `abc`
into `x` [^2]. Although contrived, this shows the issue at hand.

Why is it an issue you might ask?

Doc strings, comments, and linters depend on a specific spacing of characters. If a
ligature font comes in and changes that, then your indentation can get off, causing
minor readability issues for you and other developers later on.

> There are plenty of ligature fonts which maintain the same amount of space, though
> it is important to note that not all of them do. Some people are very picky about
> things being all lined up, myself included.

## Making Edits Can be Harder

Since the font changes the glyph being rendered, when you go to modify the characters
that make up the ligature, it will switch back to the original version. This can be
quite jarring at times, despite being very similar looking.

Obviously, it is pretty easy to remember that the `!` in `!=` is on the left, but with
a ligature, it can be rendered in the middle, requiring a slight mental reminder to
position your cursor a little bit more to the left. If you use Vim, and want to go right
to a specific character, this might be a bit weird, since it is in between 2 columns.

## Sometimes They Are Just Plain Weird

Some ligatures display `|>` as `▷`, for example, languages like F#:

```fsharp
let squareAndAddOdd values =
    values
    |> List.filter (fun x -> x % 2 <> 0)
    |> List.map (fun x -> x * x + 1)
```

Versus:

```fsharp
let squareAndAddOdd values =
    values
    ▷ List.filter (fun x -> x % 2 <> 0)
    ▷ List.map (fun x -> x * x + 1)
```

I have to agree that this ***looks*** better, but to the unaccustomed, this can just be
confusing: "Why do they use triangles here?" "Oh, they don't, that's just my font I am
using".

## Fin

Do as you please. If you like ligatures, use them! If you don't, then don't! I don't use
them, for the reasons stated above.

---

[^1]: Technically it is called a "glyph", since glyphs are the ones responsible for
actually doing the rendering, whereas the characters are the underlying
bytes being rendered.

[^2]: This sounds like a cool way to bypass government censorship (you didn't hear
that from me though).
