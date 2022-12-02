pub struct ParaCode {}
impl ParaCode {
    pub fn version(&self) -> String {
        return "3.0.0".to_string();
    }

    pub fn release_stage(&self) -> String {
        return "development".to_string();
    }

    pub fn new() -> ParaCode {
        return ParaCode {};
    }
}
