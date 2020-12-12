# ParaCode

The ParaCode Programming Language!

---

### Benefits of using ParaCode

* Open Source
* Highly Human Readable
* Cross-Platform
* Continuously Developed
* Highly Portable

---

### Getting Started
If you are using the python files, run installDependencies.py
If you are using the executable file, run the installDependencies executable

---

### Running the shell
##### There are two methods to run the shell

#### Method One:
1. Download the ParaCode Programming Language, that being
either your platform's executable file, or the python files.
2. If you download the python files, run shell.py.
If you download your platform's executable file, then run the downloaded file. (There might be an installation process here)

#### Method Two:
1. Install the ParaCode package with 
```
pip install ParaCode
```
2. In your python file, if you want to run the shell, import ParaCode with
```python
from ParaCode import shell
```
Otherwise, if you want to run ParaCode code without the shell, import ParaCode with
```python
from ParaCode import basic
```
3. If you are running the shell, add the following to your python file
```python
shell.RunShell()
```
Otherwise, if you are running ParaCode code without the shell, add the following to your python file
```python
basic.run('<stdin>', 'PRINT("Hello, World!'))
```
And of course, replace the second argument with the code you want to run

---

### config.toml
config.toml is a file that is required by ParaCode.
This is the default config.toml:
```ini
# Configuration For The Shell
[shell]
userColor = "white"
userStyle = "none"
consoleColor = "white"
consoleStyle = "none"
pointerColor = "green"
pointerStyle = "none"
errorColor = "red"
errorStyle = "none"

# Configuration For ParaCode
[lang]
packagePath = "Packages/"
```

### preferences.toml
preferences.toml is a file that is not required by ParaCode, but will be created when you run a command like `RUN("HelloWorld.para")` in the shell.
It is used by ParaCode to run the correct file when you execute the command `RUN` in the shell.

---

### Examples
All of the following examples can be found in the Examples Folder
If you are using the ParaCode package, than go to the [GitHub Repository](https://github.com/DaRubyMiner360/ParaCode).
If you have an example that you would like to submit, [Email Me](mailto:darubyminer360@gmail.com), or submit a pull request.

# 

### To run a ParaCode file (the file extentions are .para and .paracode) through code, create the file, and run
```
RUN("HelloWorld.para")
```
And replace HelloWorld.para with the file name

On windows, you can also just open the ParaCode file and it will automatically open in the shell and run

# 

### Comments can be any of the following
```
# This is a comment like Python's
// This is a comment like many other languages
; This is a comment like Assembly's
```

# 

### Printing in ParaCode is a simple as using one of the following
```
// For Without Color
PRINT("Hello, World!")
ECHO("Hello, World!")

// For Color
PRINT("Hello, World!", "Blue")
ECHO("Hello, World!", "Green")
PRINTCOLOR("Hello, World!", "Yellow")
ECHOCOLOR("Hello, World!", "Red")
```

# 

### Variables
Variables can be created and set with either the `VAR` keyword or the `VARIABLE` keyword.
Example:
```
VAR string = "Hello, World!"
PRINT(string)
VARIABLE string = "!dlrow, olleH"
PRINT(string)
```

# 

### Functions
Functions can be created with either the `FUNCTION` keyword or the `FUNC` keyword.
Example:
```
FUNCTION sayHello(name)
    PRINT("Hello, " + name + "!", "RED")
END

FUNC sayHello2(name)
    PRINT("Hello, " + name + "!", "RED")
END

sayHello("Bob")
sayHello2("Jerry")
```

# 

### Creating, Deleting, Writing To, And Reading From Files
You can create a file with `CREATEFILE(fileName)`
Example:
```
CREATEFILE("text.txt")
```

You can delete a file with `DELETEFILE(fileName)`
Example:
```
DELETEFILE("text.txt")
```

You can write to a file with `WRITEFILE(fileName, textToWrite)`
Example:
```
WRITEFILE("text.txt", "test")
```

You can read from a file with `READFILE(fileName)`
Example:
```
READFILE("text.txt")
```

You can append text to a file with `APPENDFILE(fileName, textToWrite)`
Example:
```
APPENDFILE("text.txt", "test")
```

# 

### Time and Date
You can get the year with `GETYEAR()`
Example:
```
PRINT(GETYEAR())
```

You can get the month with `GETMONTH()`
Example:
```
PRINT(GETMONTH())
```

You can get the day with `GETDAY()`
Example:
```
PRINT(GETDAY())
```

# 

### Input
You can input with `INPUT`
Example:
```
VAR input = INPUT("Name >> ")
PRINT(input)
```

# 

### Colors
You can use colors with the corresponding name, or you can use the hex value

---

### Hello, World Application:
```
PRINT("Hello, World!")
```

---

### Discord.para
You can create a Discord Bot using ParaCode using the built-in Discord.para API.
To get started, add `DISCORDTOKEN(token)` to set the token, or later, when running the bot, add the token as a parameter.
Add `VAR client = DISCORDCLIENT()`