pub struct LogColor {}
impl LogColor {
    pub fn default() -> String {
        return "\x1b[0m".to_string();
    }
    pub fn error() -> String {
        return "\x1b[31;1m".to_string();
    }
    pub fn warning() -> String {
        return "\x1b[33m".to_string();
    }
    pub fn info() -> String {
        return "\x1b[34m".to_string();
    }
    pub fn bold() -> String {
        return "\x1b[1m".to_string();
    }
}

// fixiter
