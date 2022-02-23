### Enums

Enum is short for enumeration, which is a set of constant
and unique members. These members are all instances of the
parent enum type.

An enum might look something like:
```typescript
let ExampleEnum = Enum.extend({
    name = 'ExampleEnum'

    instance = {}

    HELLO = 0
    WORLD = 1
});
```

Then, to actually use the enum, you can use either of the following:
```typescript
let v = ExampleEnum.new(ExampleEnum.HELLO);
```

or

```typescript
let v: ExampleEnum? = ExampleEnum.HELLO;
```
