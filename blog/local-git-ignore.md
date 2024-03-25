# How to Hide Files In Git Locally

This is a very small tip on how to cleanup your `.gitignore` files.

Usually you just add everything that you want to ignore from version control into the `.gitignore` file,
and all is well. But what happens when you want to ignore a certain file or folder, and it only applies to your current
setup, or your current IDE? You shouldn't need to pollute the `.gitignore` file in version control because
you want to hide something locally.

To fix this, look no further then the `.git/info/exclude` file! If you `cat` it out, it will explain itself:

```
# git ls-files --others --exclude-from=.git/info/exclude
# Lines that start with '#' are comments.
# For a project mostly in C, the following would be a good set of
# exclude patterns (uncomment them if you want to use them):
# *.[oa]
# *~
```

Just like your `.gitignore`, just add a line for each file you want to ignore, and only your system will be affected!

As an added bonus, if there is a list of files you want to hide (locally) across many projects, you can
add them to your `~/.config/git/ignore` file instead!
