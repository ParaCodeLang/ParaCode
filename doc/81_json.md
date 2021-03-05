### JSON reading and writing

You might also want to use JSON files, 

To load json text into a dictionary, use the `Json.loads` method.

Example:
```javascript
let json_string = "
{
    "researcher": {
        "name": "Ford Prefect",
        "species": "Betelgeusian",
        "relatives": [
            {
                "name": "Zaphod Beeblebrox",
                "species": "Betelgeusian"
            }
        ]
    }
}
";
let data = Json.loads(json_string);

Console.write(data);
```

To write a valid json dictionary to a file, use the `File.write` method.
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
