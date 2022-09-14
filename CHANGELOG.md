# Changelog
All notable changes to this project will be documented in this file.

The format a slightly altered version of [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## A Look to the Future
- Shorts, unsigned shorts, unsigned integers (uint), longs, unsigned longs (ulong), and doubles
- Support for variables in the `catch` statement
- More error messages
- The ability to use keyword arguments when calling a function
- **kwargs (Keyword Arguments)
- More exceptions
- Complete requests HTTP module
- An entire interfacing module for ParaCode/C++ communication
- A reflection module
- A graphics module
- Tab completion in the repl
- A better icon

## [3.0.0] - CURRENTLY UNRELEASED
### Changed
- Ported the entire language to C++
- Converted the examples and documentation to use C++ instead of Python
- `Time.sleep` now takes in milliseconds instead of seconds
- Moved scripts (build, dataCounter, etc.) into the `scripts` directory

### Removed
- Everything related to NumPara, SciPara, or Tk. Replacements might be added in the future.

## [2.1.0] - CURRENTLY UNRELEASED
### Added
- Easy use of default parameters in functions
- *args (Non-Keyword Arguments)
- Complete regex support
- Some basic exceptions
- Enums

### Changed
- Made the repl slightly nicer to look at
- Made dictionaries more internal.

### Fixed
- Fixed TimeDelta not working with optional arguments
- Fixed scenarios like `my_number != null && my_number > 0` crashing from the right side being evaluated even when the left side is false

### Removed
- PCPM executable (in the future, it will be installed via the ParaCode Installer)
- `installDependencies.py` as it has been unneeded for quite a while

### Security
- PCPM now supports publishing packages securely. For examples on how to implement this in a package repository, see the changes made to the CDN

## [2.0.1] - 2021-10-18
### Fixed
- Fixed what happens when using `||` and `&&` if you had an expression after the operators. If you ran `"A" == "A" || "A" == "B"`, it would interpret it as `("A" == "A" || "A") == "B"`, so it would return false instead of true.
- Fixed multiline comments not working correctly when used in certain places
- Fixed multiline comments breaking the repl

## [2.0.0] - 2021-10-9
### Added
- Standard library written largely in ParaCode itself
- Repl
- PCPM (ParaCode Package Manager)
- Documentation
- More, higher quality, examples
- Update script
- `try`/`catch` statements and exceptions
- New types and aliases
- Basic interfacing with python code from ParaCode

### Changed
- Completely rewrote the language as an OOP language
- Separated everything into multiple files
- Improved `import` statement drastically

### Removed
- `shell.py` file
- Unnecessary files

### Security
- PCPM package uploading doesn't require a login

[3.0.0]: https://github.com/ParaCodeLang/ParaCode/compare/rewrite...rewrite-cpp

[2.1.0]: https://github.com/ParaCodeLang/ParaCode/compare/2.0.1...rewrite
[2.0.1]: https://github.com/ParaCodeLang/ParaCode/compare/2.0.0...2.0.1
[2.0.0]: https://github.com/ParaCodeLang/ParaCode/releases/tag/2.0.0
