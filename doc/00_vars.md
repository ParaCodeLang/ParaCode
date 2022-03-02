### How to declare and use variables

To get started with variables,
use the `let` keyword. To use
`let`, we give the name we
want to be associated with
the variable, as well as an
optional type, such as `int`,
`float`, or `str`.

For example:

```typescript
let mynum: int = 5;
```

Creates a variable named mynum,
with a type of `int`, and assigns
its value to 5.

Then, if you want to allow the
variable to attempt to auto-cast
to the given type, you can add
a `?`

Here's an example from the
enum documentation:

```typescript
let b: ExampleEnum = ExampleEnum.HELLO;
```

wouldn't work because `ExampleEnum.HELLO`
is actually an integer, but

```typescript
let b: ExampleEnum? = ExampleEnum.HELLO;
```

*would* work because it is allowed to
use the constructor.
