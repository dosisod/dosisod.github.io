# NPM: Not Much Performance

This blog is about how slow JavaScript is, and how certain maintainers have resorted
to writing faster tools in Rust, Zig, and Golang, instead of JavaScript [^1]. I find it ironic
that NPM is being used distribute binary blobs given that NPM is a JavaScript ecosystem [^2].

Here are a few examples:

* [SWC](https://swc.rs/): A TypeScript/JavaScript compiler written in Rust
* [esbuild](https://esbuild.github.io/): A JavaScript bundler written in Golang
* [Parcel](https://parceljs.org/): Another JavaScript bundler written in Rust
* [Snappy](https://www.npmjs.com/package/snappy): A fast compression library written with [NAPI-RS](https://napi.rs/) (Rust)

Note how most of these are tooling focused: Most are targeted at compilers, which
will be used by your bundlers, type-checkers, and transpilers ([Vite](https://vitejs.dev/) is a popular
example of this).

The reason we are seeing a emphasis on faster tooling is because these fast binaries serve
no purpose to the end user: You can't deploy a Rust/Go/Zig binary to the user.
Another reason is because NodeJS is still the primary server-side JavaScript framework:
Frameworks like [Deno](https://deno.land/) and [Bun](https://bun.sh/) have yet to take off,
and catering to the largest audience, NodeJS, makes the most sense for most tool-makers.
Lastly, there is a plethora of software on NPM, not all of which is supported in Deno/Bun.

## Will There Be A Future Without JavaScript?

Hardly. Some will say C, Java, Visual Basic, and FORTRAN are dead languages, but there is
plenty of depended-on code written in these languages, and they won't be going away anytime
soon [^3].

Sometimes people don't care about performance, and (sometimes) that is fine! Worry about
building good software that serves a purpose, don't make fast software that goes nowhere.

---

[^1]: Yes, I know: JavaScript is a language. NodeJS is a runtime, and NPM is a package
manager. They are often used together, but not all JavaScript code comes from NPM, and
not all JavaScript is executed using NodeJS. Still, NodeJS remains the biggest framework out
there, and that is the ecosystem I will be talking about today.

[^2]: Also, some alarm bells should be going off at the thought of any ole' NPM package
being able to plop a malicious executable on your machine. I don't know if there is any
automated scanning of NPM packages, but I doubt there is.

[^3]: C and Java will never die. C is used in more places then you might think, and Java is
taught far and wide, and will never not be talked about. Until Kotlin takes over the world,
perhaps.
