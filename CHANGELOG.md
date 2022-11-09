# Changelog
All notable changes to this project will be documented in this file.

The format a slightly altered version of [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## A Look to the Future
- Support for variables in the `catch` statement
- The ability to use keyword arguments when calling a function
- **kwargs (Keyword Arguments)
- More exceptions & error messages
- An entire interfacing module for ParaCode/Rust communication
- A superior, modular language structure allowing for true extension creation (ie. lower-level methods written in Rust for use in ParaCode or even custom keywords and operators)
- A complete requests HTTP module
- A graphics module
- A more advanced unit tests module
- Tab completion in the repl
- A better icon

## [3.0.0] - CURRENTLY UNRELEASED
### Changed
- Ported the entire language to Rust
- Converted the examples and documentation to use Rust instead of Python
- `Time.sleep` now takes in milliseconds instead of seconds
- BasicValue is now a Rust `trait` and all primitive types implement it. There's also a BasicWrapper type that acts as a container for values, objects, and types.
- Moved scripts (build, dataCounter, etc.) into the `scripts` directory
- Separated the language and repl to be mostly independent

### Removed
- Everything related to NumPara, SciPara, or Tk. Replacements might be added in the future.

## [2.1.0] - CURRENTLY UNRELEASED
### Added
- Easy use of default parameters in functions
- *args (Non-Keyword Arguments)
- Complete regex support
- Some basic exceptions
- A reflection module
- A basic unit tests module
- An events system
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
- PCPM now supports publishing packages more securely and supports authentication. For examples on how to implement this in a package repository, see the changes made to the CDN

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

[3.0.0]: https://github.com/ParaCodeLang/ParaCode/compare/rewrite...rewrite-rust

[2.1.0]: https://github.com/ParaCodeLang/ParaCode/compare/2.0.1...rewrite
[2.0.1]: https://github.com/ParaCodeLang/ParaCode/compare/2.0.0...2.0.1
[2.0.0]: https://github.com/ParaCodeLang/ParaCode/releases/tag/2.0.0
