### Dictionary operations

In your code, you may want to store multiple
contiguous objects together, indexed by *keys* that can be any type. Unlike arrays, which are indexed by a range of numbers, dictionaries are indexed by those *keys*. Dictionaries let you do this in a way that won't clutter up your code with
lots of related variable names.

Here's an example of how to create a dictionary and assign
it to a variable.

`let names = Dictionary.new(['Jeffrey', 'Sam', 'Buddy'], ['Williams', 'Johnson', 'White']);`

The `names` dictionary holds three strings, each
representing a name.

If you want to loop over these names, you can use `for`.

```javascript
for name in names {
    print(name);
}
```

Prints:
```
[Jeffrey, Williams]
[Sam, Johnson]
[Buddy, White]
```

To access a specific item in a dictionary by index, use the
access operator (square brackets)

`print(names["Sam"]); // prints ['Sam', 'Johnson']`

Dictionary have multiple methods, including ways of checking whether
an object is contained by the dictionary, appending new items to
a dictionary, and more.

```javascript
names.contains('Buddy'); // false
names.containskey('Buddy'); // true

names.append(['Tiffany', 'Jones']); // names is now {'Jeffrey': 'Williams', 'Sam': 'Johnson', 'Buddy': 'White', 'Tiffany': 'Jones'}

names | Dict.new(['Sam', 'Johnson'], ['Tyler', 'Scotts']); // returns {'Jeffrey': 'Williams', 'Sam': 'Johnson', 'Buddy': 'White', 'Tyler': 'Scotts'}

names & Dict.new(['Sam', 'Johnson'], ['Tyler', 'Scotts']); // returns {'Sam': 'Johnson'}
```
