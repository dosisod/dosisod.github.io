# Comments on the Stack Overflow 2022 Survey

Every year, I read the Stack Overflow survey as soon as it comes out.
I ditched Facebook, and never used Twitter, and in general, don't use
social media [^1], so it is always nice to see the general trends in the
tech world.

This is going to be quite opinionated, or, more specifically, have no general
direction, and will basically me just writing down my thoughts on this years
survey (see title).

Let us begin!

## [Online course platforms to learn how to code](https://survey.stackoverflow.co/2022/#section-learning-to-code-online-course-platforms-to-learn-how-to-code)

What stuck me as interesting about this is that there is no reference to
[freecodecamp](https://www.freecodecamp.org/). Their curriculum is
[100% open source](https://github.com/freeCodeCamp/freeCodeCamp), and I often
see it referenced on GitHub trending.

I also expected to Youtube to be on here, perhaps these 2 got grouped into the
"other" category? Who knows.

## [Developer type](https://survey.stackoverflow.co/2022/#section-developer-roles-developer-type)

I find it kinda sad (not really) that most people fall into the "full stack" or
"front/back-end" category. As a full-stack developer myself (who does other programming
things as well), I have come to realize that there is more to programming then the typical:

```
Take data from website -> Send to API -> Validate -> Store in database
```

cookie cutter applications.

Why not build better tooling, better testing frameworks, faster build systems, better
package management systems, and so on? There is more to programming then just full-stack work!


## [Most popular programming, scripting, and markup languages](https://survey.stackoverflow.co/2022/#section-most-popular-technologies-programming-scripting-and-markup-languages)

As per usual, JavaScript tops the charts. Still, it is interesting that 32% of people "learning to code" are
using C, and 35% are using C++. Perhaps this is due to University students learning C/C++?

## [Most popular databases](https://survey.stackoverflow.co/2022/#section-most-popular-technologies-databases)

Postgres is awesome, and it deserves the top spot (among "Professional Developers", that is).
Postgres feels like it was designed for humans to use, compared to something like MSSQL (it is
a little quirky). Also, Postgres being open source is a huge plus for me!

Also, Redis is gaining a lot of popularity, and I think we will see the fall (or at least diminishing)
dogma around "always use a RDBMS". Redis is super-lightweight, and really makes you think about your
data: the lifetime of your data, how you want to access it, and so on.

## [Most popular "other tools"](https://survey.stackoverflow.co/2022/#section-most-popular-technologies-other-tools)

Docker is a must have in this day and age. Honestly, I don't know how I did things before Docker.
Kubernetes (k8s) is also rising in popularity, but I don't know how essential it is to the
average developer, especially those learning to code.

## [Most popular IDE](https://survey.stackoverflow.co/2022/#section-most-popular-technologies-integrated-development-environment)

Let me just take this moment to say that Vim, combined with Neovim, has a higher marketshare then IntelliJ!
I have proudly been using Neovim for a while now (and [VSCodium](https://github.com/VSCodium/vscodium) for
certain tasks), and like all Vim users, I think everyone should give it a shot [^2].

## Most loved, dreaded, and wanted

Oh boy! These are always my favorite:

### [Programming, scripting, and markup languages](https://survey.stackoverflow.co/2022/#section-most-loved-dreaded-and-wanted-programming-scripting-and-markup-languages)

As the title says, Rust is on it's 7th year as the most loved language. I love Rust. I think Rust is
the future, but who am I kidding.

What I also find interesting is that Elixir and Clojure (functional languages) are right behind Rust!
You have to go waaaay down the list to find JavaScript, which is slightly ahead of F#, another functional
language! In general, functional languages are the future. I think we (by and large) are burned out with
they typical OO languages, and looking over the horizon, we see lots of languages which are switching it
up. The water is warm, and the grass is green!

Also, Rust, TypeScript, and Python are the top 3 on the "wanted" category, all of which have very strong
type support (if you do it correctly). I also think we are starting to see the rise in statically typed
languages, or at the very least, type annotations in dynamic languages.

### [Databases](https://survey.stackoverflow.co/2022/#section-most-loved-dreaded-and-wanted-databases)

Postgres and Redis are the most loved databases. Like I said, they deserve it. Moving on...


### [IDE](https://survey.stackoverflow.co/2022/#section-most-loved-dreaded-and-wanted-integrated-development-environment)

Neovim takes the cake for the most loved IDE (83%) for a second year! Vim also is a few steps ahead of
GoLand and IntelliJ, both JetBrains products.

> I do use JetBrains products, if you consider the [JetBrains Mono font](https://www.jetbrains.com/lp/mono/) a product :)

### [Asynchronous tools](https://survey.stackoverflow.co/2022/#section-most-loved-dreaded-and-wanted-asynchronous-tools)

From what I can tell, [monday.com](https://monday.com) is a very flexible, easy to use platform.
Though I have never used it, I find it interesting that it is the most dreaded one on the list.

## Worked with vs. want to work with

In general, I find these graphics cool to look at, but not super helpful. I think it is cool
to know what people are wanting to learn, given what technologies they already know. But, in
general, "going with the flow" isn't what I will be looking for when I choose the next
technology I will be working with.

## [Top paying technologies](https://survey.stackoverflow.co/2022/#section-top-paying-technologies-top-paying-technologies)

Wow! Clojure, Erlang, F#, and LISP (all functional languages) make up the top 4 highest paying jobs!
In 6th place is Elixir, another functional language.

It would also seem that JavaScript developers can boost their salaries by $5k if they learn TypeScript.

I don't know how exactly this was calculated, since most developers will know more then just one language.

People using Neovim or Vim as their IDE make (on average) more then those using Rider, CLion, IntelliJ, and
VSC (though not as much as Emacs users!)

## [Version control systems](https://survey.stackoverflow.co/2022/#section-version-control-version-control-systems)

97% of professional devs are using VCS. This is good news!

## [Interacting with version control systems](https://survey.stackoverflow.co/2022/#section-version-control-interacting-with-version-control-systems)

Most professional devs (85%) use the command line. This is also good news! The command line gives you infinite control
over Git compared to what your IDE will use.

> Also, who uses the GitHub/GitLab/Bitbucket web interface to do their Git operations? There is nothing **wrong** with
> it, but it will seriously cramp your workflow if you have to push your code up before you can merge/branch/tag something.

## [Version control platforms](https://survey.stackoverflow.co/2022/#section-version-control-version-control-platforms)

I have always found that GitHub has the best developer experience, and the data shows it.
In fact, GitHub is the only platform where people are more likely to use it for personal projects then
work projects (none of the other platforms can say the same). And, GitHub is about twice as popular as
the next competitor, GitLab.

## [Daily time spent searching for answers/solutions](https://survey.stackoverflow.co/2022/#section-productivity-impacts-daily-time-spent-searching-for-answers-solutions)

It must feel really good (for the 10% of people) who only search 15 minutes a day for answers!
Either I'm doing something wrong, their doing something right, or they don't spend a whole lot of time coding.
Maybe I just spend a lot of time reading documentation, always trying to find a better way to do things?

## [Developer Experience: Processes, tools, and programs](https://survey.stackoverflow.co/2022/#section-developer-experience-developer-experience-processes-tools-and-programs-within-an-organization)

70% of people use CI/CD, and 58% of people use automated testing. These numbers are too low! We certainly need more
people testing their code, as do we need people who use code (ie, GitHub Actions) to lint, test, and release their code.

## Fin

That's it! Nothing too fancy, just my inputs on this year's survey.

---

[^1]: Except Stack Overflow, it seems

[^2]: Even if you don't like Vim/Neovim itself, you can always install Vim keybindings for your
IDE, which is what I do for VS Code.
