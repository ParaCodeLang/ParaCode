pub mod language {
    pub struct ParaCode {
        pub version: String,
    }

    impl Default for ParaCode {
        fn default() -> Self {
            Self { version: "3.0.0".to_string(), }
        }
    }

    /*impl ParaCode {
        fn version() -> String {
            return "3.0.0".to_string();
        }
    }*/
}
