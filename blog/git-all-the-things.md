# Git All The Things!

[Git](https://git-scm.com/) is an amazing tool! If you are a developer, you almost
certainly use it on a day-to-day basis. Git holds your code. Git tracks your changes.
Git enables for easier collaboration between developers. Git can even let you travel
(backwards) in time, and let you see what your code looked like last commit, last week,
or last release.

So why do we only use git for code?

## Git Todo Tracking

Why not use git to track your todo items? You can use it for other similar things as well:

* Grocery lists
* Journaling
* Calorie tracking
* Calendar

You can get as creative as you want! Make as many commits as you need, no one will
see this. Don't even worry about writing a good commit message: If you are making
small enough commits, you wont even need to write a commit message, as the changes
themselves will be self explanatory. Use `git log -p` to log the commits with
the changes attached.

## Git Logging

Depending on what you are logging, and how often you expect things to change, you
can write a bot which makes commits to a git repository for you. If you are subscribed
to any pushes to the `master` branch, whenever a commit is pushed, you get a notification! No
need for setting up a Slack or Discord bot!

## Git Prototyping

Creating a prototype? Testing out a new library? Try making micro commits as you go,
no more then 15-30 minutes between commits. If something doesn't work out, or you
get stuck, just wipe out your unstaged work, and go back to the most recent commit.
It feels good to just wipe the slate clean, go back to a known working state, and try
again, approaching things at a different angle.

## GaaD (Git as a Database)

Don't use in production. But in all seriousness, you could use git as a DB to store:

* Small file uploads
* Temporal metadata
* Human readable plain-text files
* Edit history to files stored in another location
* Transactional logs
* Feed syndication (using branches)
* Configuration files
* Event sourcing

Obviously use this with caution. But, if you are in a pinch, feeling ambitious, or
like using tools for purposes other then what they are indented for, you might want
to give this a try.

## Git Social Media

Why not use a git repo as a social media platform? People can pull down `master`, and
see the curated "content", or checkout other branches to see user submitted content
which could get over-looked.

Imagine a git repo where each commit is a unique file, post, or blog. You can always
checkout the `most-upvoted` or `breaking-news` tag, and see the relevant file/post/blog
for that tag.

You could have many branches such as `trending`, `most-recent`, or `top-picks`, and a script
that will `cherry-pick` certain commits, and add them to these branches. Each branch now contains
it's own independent history, and can be viewed via `git log`.

You could view the git repo directly in your IDE or terminal, or you could make a simple
web frontend which would pull and render the content from the git repo for you. If you
are using GitHub to host your git repo, you can pull in user avatars, add timestamps,
and make it as rich as or as lean as you want it to be.

We already see these kinds of collaborative git repositories with things such as
[Awesome Lists](https://github.com/topics/awesome), where it is all curated, user submitted
content. Still, these are very locked down to a specific topic, and not very generalized.
They also use a platform like GitHub, using pull requests to submit work. Instead, you could use
write a custom backend which will automate all of this for you.

## Git Backups

Perhaps storing large files in git isn't a good idea. But, for small/medium sized files,
you could use git as a place to store archives of files, and use the git commands you
already know and love to pull out files/restore backups as needed.

You could also use git to store your dotfiles (config files), that way you can quickly
pull down your dotfile repo onto your new work/home machine and be ready to go.

## Git Decentralized File Storage

By nature, git is already a decentralized file storage. But, imagine if you have a repository
for a certain topic, or a certain group of people, and a simple frontend which is able to
push/pull files to/from these scattered git repos. Since you can have many remotes in a git,
you could ask around for updates to these repos in a P2P fashion. This would work well in a
trusted web, where everyone already knows each other (I don't think I would recommend exposing
this to the whole internet).

## Git Blockchain

In a similar fashion to the decentralized file storage, you could use a git repository as a
primitive blockchain, where everyone gets a copy of the transaction history. There are certainly
better technologies out there for this, but for something that doesn't need high throughput,
a simple git repo might do

## Git Package Management

You can also use git as a way to manage an entire packaging ecosystem. A good example of this is
[termux](https://github.com/termux/termux-packages), which is (a really good) terminal emulator
Android app, with their own packaging system. Another example is the [Arch User Repository](https://aur.archlinux.org),
which is the same thing, but for Archlinux.

## Git CRM

Use git to track random tidbits of information that you pick up, but know you will forget by
tomorrow. Use it to track important dates, upcoming meetings, random facts, contact
info, and more!

Remember you can store this information however you want. It can be all in one big file,
or split up into many plain-text files, organized into many folders.

## Git Monorepo

Create a single git repo which includes a bunch of other git repos as submodules. When you
want to clone all of the code from a single organization, all you need to do is git clone
(with some extra flags. Google is your friend).

## Git Better

Create a git repo just to play around with git! Have you ever wondered what that scary looking
git command does? Try it out in an isolated environment!

Curious what happens when you start deleting/modifying the files in the secret `.git` folder?
Create a new git repo and try it out, or copy the folder of an existing git repo, and have at
it!

## Fin

As I said before, git is a very powerful tool. You can use it for many things, some use cases
more justifiable then others. Don't be afraid of git either! It is a tool, and was designed for you
to use it easily and efficiently (and experimentally).
