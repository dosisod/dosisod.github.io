# 2022 In Review: My Most Used Commands

I spend most of my time in the terminal, so suffice to say, I run lots of commands.
I have no limit on the size of my bash history file, which means I can see every command I
have ever ran on this computer, which is super helpful when debugging system issues and
so forth [^1].

Without further ado, here are the top 15 common commands I ran this year:

| Command      | Run Count | Percentage | Notes |
|--------------|-----------|-----------:|-------|
| ***TOTAL***  | 120313    |    100.00% | All the commands I ran |
| gs           | 18130     |     15.06% | Alias for `git status` |
| v            | 8631      |      7.17% | Alias for `nvim` (Neovim) |
| cd           | 6966      |      5.79% |       |
| ls           | 6934      |      5.76% |       |
| make         | 4650      |      3.86% |       |
| p3           | 4511      |      3.75% | Alias for `python3` |
| git          | 4128      |      3.43% |       |
| gcm          | 3521      |      2.93% | Alias for `git commit -m` |
| refurb       | 3454      |      2.87% |       |
| ./pre-commit | 3415      |      2.84% |       |
| pytest       | 3342      |      2.78% |       |
| gau          | 3261      |      2.71% | Alias for `git add -u` |
| gd           | 3031      |      2.52% | Alias for `git diff` |
| ./m          | 1987      |      1.65% | [^2]  |
| sudo         | 1862      |      1.55% |       |
| ***OTHER***  | 42490     |     35.32% |       |


What surprises me the most is how much I ran the `gs` command. I very often find myself
typing `gs` before and after adding files to make sure they were actually added, or just
seeing what has changed in a folder. It also makes sense that `cd` and `ls` are very close
to each other because I almost always run `ls` after `cd`ing into a directory.

Something that you will also note is how short these commands are: Compare `gs` to `git status`,
which is 8 characters longer: multiplying those mere 8 characters 18130 times will result in 140k
more keystrokes over the course of an entire year! Not only do you save time by typing less, you reduce
your chances of mistyping a command, further increasing your efficiency.

## Fin

This blog was primarily just for fun, as well as a way of satisfying my own curiosity.

---

[^1]: In addition, it is really nice to do a reverse search on every command you have
ran since the beginning of time. Don't use the built-in reverse search function in bash
though, use [fzf](https://github.com/junegunn/fzf) instead.

[^2]: This was a shell script I used for my [Skull](https://github.com/dosisod/skull)
project, and essentially acted as a `pre-commit` file.
