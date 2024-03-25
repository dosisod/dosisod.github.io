# ABI Safe Field Renaming In C/C++

This idea popped into my head recently: Could you use unions in C/C++ to safely
rename a field in a struct [^1]? Let's find out!

Imagine you have a simple `struct` called `Item`. It has a few fields, `name`, `price`,
and `upc_code`:

```c
struct Item {
    const char *name;
    float price;
    const char *upc_cod;
};
```

All is good, except you made a typo and spelled `upc_code` as `upc_cod` instead. Oops. It doesn't help
that you shipped this to your clients 2 versions ago, and you can't exactly
fix it without forcing them to change their code and re-build.

But what if we used a union?

Normally unions are meant for storing different data types under different names while
occupying the same amount of memory. But, nothing is stopping you from defining multiple
names with the same data type! So, you can do something like this:

```c
struct Item {
    const char *name;
    float price;
    union {
        const char *upc_cod;
        const char *upc_code;
    };
};
```

And volià! Now your clients can use the both the old and the new fields at the same time
without breaking ABI.

We can take this a step further though by using an annotation to deprecate the
old field and pusing our users to use the new field [^2]:

```c
    union {
        [[deprecated("Use `upc_code` instead")]]
        const char *upc_cod;
        const char *upc_code;
    };
```

This will give your users a nice error message when they try to use `upc_cod`:

```
main.c:20:12: warning: 'upc_cod' is deprecated: Use `upc_code` instead [-Wdeprecated-declarations]
    puts(i.upc_cod);
           ^
```

---

[^1]: You can tell I think about programming-related things a lot

[^2]: Use `__attribute__((deprecated))` for C. You could also wrap this in a
macro which conditionally uses the C/C++ version depending on whether
`__cplusplus` is defined.
