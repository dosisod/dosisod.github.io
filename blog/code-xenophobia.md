# Code Xenophobia

> Xenophobia: fear and hatred of strangers or foreigners or of anything that is strange or foreign [^1]

When you see a coding project that doesn't come from GitHub, do alarm bells sound off in your head?
When you are taken to a Source Forge download page, do you run away?
Do projects that live on Gitlab or some other self-hosted Git instance make you weary or annoyed?
Are projects written in languages that you don't like (for example, PHP, C, or Perl) justification for
discarding it and looking for a different project?

If you answered to "yes" to any of the previous questions, you might be suffering from "Code Xenophobia".

## How It Hurts

For many Open Source contributors, contributions are voluntary, and more often than not, thankless.
In their free time they write their code, give it to the world free of charge, and what do you [^2]
do? You ignore or discredit it because they host it on the "wrong" platform, or because they wrote it
in the "wrong" language: Maybe it is a language you don't even know, but have heard is bad, therefore,
anything written in it must be bad.

I must make it clear though that there are valid reasons for ignoring a project because of the language it
is written in:

* You need a library that is written in/compatible with your language
* Your hardware, OS, etc doesn't support it
* You need a solution now and don't have time to setup a new toolchain

In (most) other instances though, you are free to choose whatever you want, and as such, should not disregard
a perfectly valid project just because your initial assumptions might tell you otherwise.

In addition, many developers (especially new ones) don't know or don't care about what is popular
or what everyone else is using, and just does the best that they can with what they know or have been
told. They shouldn't have to suffer the consequences of learning the "wrong" language, or hosting
their code on the "wrong" platform that "nobody" uses anymore.

## Why Do We Do It?

Humans are protective animals: We protect what we deem important, and reject what we deem unsafe.
When it comes to code though, sometimes we only feel safe when we are in our code habitat, and for
a lot of us, that habitat is GitHub. Anything non-GitHub is scary, "insecure", or untrustworthy.
We have been told that GitHub is [secure](https://github.com/security): Dependabot notifies you
when security vulnerabilities crop up, secret scanning prevents secrets from getting leaked,
and there are a bunch of flags and such which allow you to lock down your repo, among many other
awesome features. These are all great features. Some platforms don't have all of these features
though. This doesn't make the platform any lesser, especially from the perspective of the devs
who use them on a day-to-day basis.

Humans are territorial animals: We have a place we call home, and we feel the need to defend it
and built it up, rejecting anything which is not in our territory. Everyday GitHub gets more and
more users, and the total number of repositories on the platform goes up and up. This is not a
bad thing by any means, it simply means that the territory that we (GitHub devs) inhabit grows
and grows, further imprinting this idea that GitHub is good, and non-GitHub is bad.

Humans aren't the best at logical induction: The difference between "***All*** projects on Source Forge
are low-quality" is very different than "***A lot*** of projects on Source Forge are low-quality".
With the former, only one high-quality project is needed to disprove the statement. Whenever you use
start a phrase with the words "any", "all", "every", or "most", you better make sure it won't be
something stupid [^3].

Humans are lazy: Nobody has the time to sit and audit all the code for a new library or project,
and so we let our biases do the initial filtering. Sometimes this filtering can filter out too much.

## How To Stop It

Try to be a bit more introspective when you are looking for projects:

* Why exactly am I using/not using this project? Is there a good reason? Imagine you have to fill out an exit survey every time you turn down a project, essentially telling the developer why you chose not to use their project.
* Do my fears have any foundation? Is it an initial, impulsive fear, or a truly valid concern?
* Would I still use it if it was written in language X, or hosted on platform Y?
* Think: ***What is the worst that could happen if I run this?*** Chances are, nothing seriously bad will happen.

## Fin

Thanks for listening to my rant.

---

[^1]: [](https://www.merriam-webster.com/dictionary/xenophobia)

[^2]: Probably not ***you***, but maybe you.

[^3]: I could (and probably will) write an entire blog post on how destructive this sort of thinking
can be, since it touches multiple different areas including politics, cliques, cognitive dissonance,
social media indoctrination, and so much more.
