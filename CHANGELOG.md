# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Support for variables in the `catch` statement
- More error messages
- Complete requests HTTP library
- Better interfacing with python code from ParaCode
- The ability to use keyword arguments when calling a function
- **kwargs (Keyword Arguments)
- More exceptions

## [2.1.0] - CURRENTLY UNRELEASED
### Added
- Easy use of default parameters in functions
- *args (Non-Keyword Arguments)
- Complete regex support
- Enums

### Changed
- Made the repl slightly nicer to look at

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

[Unreleased]: https://github.com/DaRubyMiner360/ParaCode/compare/2.1.0...HEAD
[2.1.0]: https://github.com/DaRubyMiner360/ParaCode/compare/2.0.1...2.1.0
[2.0.1]: https://github.com/DaRubyMiner360/ParaCode/compare/2.0.0...2.0.1
[2.0.0]: https://github.com/DaRubyMiner360/ParaCode/releases/tag/2.0.0
