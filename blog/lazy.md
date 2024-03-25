# Lazy Loading Images Without JavaScript

I don't like JavaScript, or, more accurately, I try to avoid it whenever possible.

[In my most recent blog](./film/2023-july-bellevue/index.html) though I ran into an
issue where I needed to load a bunch of images (36, it was from a film shoot),
and doing so up front would be very inefficient. The best option would be to lazy-load
the images, but from what I have experienced, this required JavaScript.

Me being the JavaScript unenthusiast I am I looked up if there was a way to do this
in plain HTML. Turns out you can, and it's really easy!

```html
<img src="some_image.png" loading=lazy />
```

And that's it! Well, not quite.

The first time I did this it immediately loaded 28 of the 36 images, which was not what
I expected. Turns out that when you don't specify an image size the browser has no idea
how big the image is, and thus how big the viewport is.

To fix this, hard-code the size of the image:

```html
<img src="some_image.png" width=1920 height=1080 loading=lazy />
```

And now your images should load at a more modest rate.

## Next Steps

Since I am getting into film more I'm looking into experimenting more with different
loading techniques. I know that there image attributes called [`srcset`s](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/srcset)
that change the image based on the size of the screen, which would be good for mobile (and, no JavaScript!).

Another (albeit unrelated) technique that I want to explore is [Blurhashes](https://blurha.sh/).
They are basically very approximate gradients that look like the blurred version of the
image you want to look at. If I had some sort of pay walled app or dynamic image loading
feature I would find this really useful, though I doubt I will have a concrete need for it
anytime soon.
