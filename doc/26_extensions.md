### Extensions

`WARNING: This page of documentation is work-in-progress
and is likely almost entirely going to change in the future!`

Many languages support the creation of custom extensions to
the language itself at a lower level. In ParaCode, which
tries to be as extensible as possible, there are a variety
of ways to extend different parts. The main way, however, is
using extensions.

`NOTE: While some parts can be extended via Python, the 
functionality is limited. Extensions are only available
in Rust versions (v3.0.0+).`

To start development on an extension, you will need a
library crate. These are created via:
```bash
cargo new --lib extension_name
```
<!-- TODO: Explain what the command does -->
<!-- TODO: Cargo.toml: Say to add paracode as a dependency and show
how to add paracode-macros as well -->
<!-- TODO: Cargo.toml: Say to change the type of produced library? -->
<!--Then, inside your `Cargo.toml` file,-->
<!-- TODO: lib.rs: Show how to use ParaCode's extensions API -->
<!--Then, inside your `src/lib.rs` file,-->
<!-- TODO: Demonstrate how to load and use the exposed methods
and types from inside ParaCode -->
<!-- TODO: Show how to build the extension -->
