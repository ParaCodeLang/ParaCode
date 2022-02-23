### Random number generation

ParaCode includes a module for generating random numbers, `std/math/random`.
You can use this module to generate a random integer from a seed value or generate it from a "random seed",
or you can use the `range` method of `random` to generate a random
number from a predefined range of your choice.

Example:

```typescript
import "std/math/random.para";
print(random.range(25, 1, 1337)); /* prints 10  -- try with a different seed! */
```
