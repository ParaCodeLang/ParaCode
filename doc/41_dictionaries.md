### Dictionary operations

In your code, you may want to store multiple
contiguous objects together, indexed by *keys* that can
be any type. Unlike arrays, which are indexed by a
range of numbers, dictionaries are indexed by those *keys*.
Dictionaries let you do this in a way that won't clutter
up your code with lots of related variable names.

Here's an example of how to create a dictionary and assign
it to a variable.

```typescript
let names = ['Jeffrey': 'Williams', 'Sam': 'Johnson', 'Buddy': 'White'];
```

The `names` dictionary holds three strings, each
representing a name.

If you want to loop over these names, you can use `for`.

```typescript
for name in names {
    print(name);
}
```

Prints:
```bash
['Jeffrey', 'Williams']
['Sam', 'Johnson']
['Buddy', 'White']
```

Creating an *empty* dictionary is a little different.
Here's an example of how to create an empty dictionary
and assign it to a variable.

```typescript
let names = [:];
```

To access a specific item in a dictionary by index, use the
access operator (square brackets)

```typescript
print(names["Sam"]); // prints ['Sam', 'Johnson']
```

Dictionary have multiple methods, including ways of checking whether
an object is contained by the dictionary, appending new items to
a dictionary, and more.

```typescript
names.contains('Buddy'); // true

names.append(['Tiffany', 'Jones']); // names is now {'Jeffrey': 'Williams', 'Sam': 'Johnson', 'Buddy': 'White', 'Tiffany': 'Jones'}

names | ['Sam': 'Tyler', 'Johnson': 'Scotts']; // returns {'Jeffrey': 'Williams', 'Sam': 'Johnson', 'Buddy': 'White', 'Tyler': 'Scotts'}

names & ['Sam': 'Tyler', 'Johnson': 'Scotts']; // returns {'Sam': 'Johnson'}
```
