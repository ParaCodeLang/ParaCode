### File reading and writing

At some point in your program or script you will
likely want to make use of file input and output.
Wheather you're reading and saving configuration
files, or a user's documents, file I/O can be
very useful.

Just like the `Console` object, a `File` object is
also made available by means of the `io` module.
The `io` module is imported from the standard
`__core__` module and thus available without any
manual importing.

To write a string to a file, use the `File.write` method.
This method takes in two arguments: The path to the file
you want to write, as well as the content you want to write
to the file.

Example:
```javascript
File.write('file.txt', 'Hello world');
```

To append a string to a file, use the `File.append` method.

Example:
```javascript
File.append('file.txt', 'Hello world');
```

To create a file, use the `File.create` method.

Example:
```javascript
File.create('file.txt');
```

To delete a file, use the `File.delete` method. (Also works with directories)

Example:
```javascript
File.delete('file.txt');
```

To delete a directory, use the `File.deletedir` method.

Example:
```javascript
File.deletedir('directory');
```

To check if a file exists, use the `File.exists` method.

Example:
```javascript
Console.write(File.exists('directory'));
```

To check if a file is a file, and not a directory, use the `File.isfile` method.

Example:
```javascript
Console.write(File.isfile('file.txt')); // true
Console.write(File.isfile('directory')); // false
```

To check if a file is a directory, and not a file, use the `File.isdir` method.

Example:
```javascript
Console.write(File.isdir('directory')); // true
Console.write(File.isdir('file.txt')); // false
```

To open a file, we create `File` instance object via
the `File.open` method. An instance of the `File`
object holds the name and path of the file, as
well as the actual data it holds.

Here is an example of how to read a file into a variable.

```javascript
let file = File.open('file.txt');
let content = file.data;

Console.write(content); // write output to console
```

And here is another example of how to read a file into a variable.

```javascript
let content = File.read('file.txt');

Console.write(content); // write output to console
```

To read the lines of a file into an array use File.readlines.
```javascript
let content = File.readlines('file.txt');

Console.write(content); // write output to console
```
