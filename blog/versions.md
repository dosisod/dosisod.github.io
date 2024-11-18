# How to Version Your Code

This [xkcd](https://xkcd.com/1172) post should set the mood for the rest of the blog post:

<img src="https://imgs.xkcd.com/comics/workflow.png"><br>

Basically, it can be hard to know when a "minor" change is actually a major one, or when a
"major" change is actually insignificant. There is no one-size-fits all solution, but
there are many ways to version your code, all of them with their own ups and downs.

## Semantic Versioning [(SemVer)](https://semver.org)

For one reason or another, the internet has pretty much settled on semantic versioning as the
de-factor versioning system of the internet.
Basically, you have a bunch of numbers separated by dots like so:

```
MAJOR.MINOR.PATCH
```

In this example,

* `MAJOR` is a breaking change. Clients will need to change their code.
* `MINOR` is a backwards-compatible change (new functionality, bug fix, etc).
* `PATCH` is a bug/documentation fix, no new functionality.

Whenever you make a new release, you bump (increase) the corresponding major/minor/patch version,
and reset the number(s) to the right. For example, increasing the minor version of `1.3.5` will result in
`1.4.0`.

Optionally, when `MINOR` or `PATCH` is zero, it is dropped. For example, `2.0.0` can be written as `2.0` or just `2`.
Also, there is sometimes an optional `v` prepended to the version, ie, `v1.2`.

> Some governing bodies (Ahem, Microsoft) like to use semantic versions with 4 levels, ie,
> `1.2.3.4`. This is overkill for most applications. I've only really seen this with .NET applications
> (for the most part).

### Pros of SemVer

If done correctly, it is really nice to know if a package is just adding a small fix, and can be
updated with no real issues.

It allows you to support multiple different "timelines" of your code. For example, Python supports `3.8.x`, `3.9.x`, etc,
adding features and bug fixes to each version separately. Since they have such a large ecosystem, they have to
support many different versions of their programming language, since not everyone can/will upgrade right away.

It is very common.

### Cons of SemVer

It requires a lot of vigilance to make sure you are doing semantic versioning correctly. If you and your team are
the only ones using your code, you can get away with a bad release, but in the wild, it can be a little bit harder.
Sometimes you don't realize you have made a backwards-incompatible API/ABI change until it is too late.

Attackers can latch onto the "minor/patch versions are always safe" mindset, and release a malicious package,
only bumping the patch version. This has happened many times with NPM packages, where someone gets unauthorized access,
"takes over" a package, and pushes a malicious update [^1].

---

## Calendar Versioning [(CalVer)](https://calver.org)

Instead of versioning based on semantics, you version based on the day that version was released. For example:

```
2022.6.13
```

As you can see, we still follow the SemVer style of having dots to separate the important numbers, the only difference
being that the numbers now represent years, months and days.

> You can format the date in many different ways. You could use number of weeks since the start of the year,
> you could drop the day portion, you could use a shortened year, the world is your oyster.

CalVer is really nice in that it encodes metadata about the release in the version itself. You can tell just by
looking at it when it was released, and how long it has been since the last release.

### Pros of CalVer

Very easy to generate version numbers. In Linux, you can just use `date +%Y.%-m.%-d` to get a new version!

As mentioned before, the time metadata is really nice, and also convenient for users. In traditional SemVer, devs will have
access to the tagged commits, and can see when a tag was released. For users though, they will have to get their date info from some
other source, such as release blogs, release notes, or some other method. CalVer helps solve that.

### Cons of CalVer

Doing multiple releases a day can be challenging. You can add a forth column if you expect to have multiple releases a day, for example:

```
YEAR.MONTH.DAY.NUMBER_OF_RELEASES_TODAY
```

Also, CalVer only makes sense for libraries and applications which have a linear timeline: supporting multiple "branches" of CalVer
doesn't make sense, because any changes to these branches will be based off of semantics, not based off time.

---

## Zero Versioning ([ZeroVer](https://0ver.org/))

ZeroVer, or 0Ver, is like SemVer, but it uses a `0.` prefix. In traditional SemVer, anything below a `1.0` release
is considered "unstable". Typically, when the `v1` of a library/application is released, the API is considered stable, and ready for
production use.

ZeroVer isn't an actual versioning system, just a sub-set of SemVer, but is an anti-pattern you should look out for.

### Pros of ZeroVer

Very easy. You can be lazy as you want, as users are supposed to just accept that all your version bumps are unstable.

### Cons of ZeroVer

Some people might avoid your software if they don't think it is stable.

---

## UnoVer

I made this up. But, it is a sub-set of SemVer that I think people should consider when building applications.

Basically, you only have one
incrementing number, starting at `1` (or `v1` if you prefer). Whenever you make a change, no matter how small, you increase the number.
Anyone ingesting your application or library has 2 choices: Upgrade, or don't upgrade. If the changes are small enough, the cost of
updating your package/library is small, encouraging an ecosystem of people wanting to keep their dependencies up to date. This is
essentially a rolling-release ecosystem, where everyone is constantly updating to the newest version.

### Pros of UnoVer

Simple to follow.

Reduces the burden (on users) of having to do big version migrations every X months.

### Cons of UnoVer

Requires library authors to write API's well, and make lots of small releases.

Doesn't work with non-linear timelines, as there is only one upgrade path: forwards!

## Fin

That's it! Versioning your code is important. When you do version your code, make sure that you keep both the developers and
the end users in mind when you think of a versioning scheme.

No matter what scheme you chose, make sure to stay consistent!

Also, if you are using GitHub, you should look into using
[Dependabot](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuring-dependabot-version-updates).
Once configured, it will automatically create pull requests whenever a new package version comes out!

---

[^1]: Note that package take-overs can happen no matter the versioning system, but they are more likely to become an
issue when using SemVer. For example, in NPM, you can say "use version `1.0.x` of package `Y`", which will always
download the latest patch version when doing a fresh install (if a new patch version is available).

