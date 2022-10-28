pub mod language {
    pub struct VariableType {}
    impl VariableType {
        pub const AUTO: &str =     "auto";
        pub const INT: &str =      "int";
        pub const STRING: &str =   "str";
        pub const ANY: &str =      "any";
        pub const FUNCTION: &str = "func";
        pub const TYPE: &str =     "type";
        
        pub const ARRAY: i32 =     1;
        pub const DICT: i32 =      2;
        pub const OBJECT: i32 =    3; // Class, data structure, etc.
    }
}
