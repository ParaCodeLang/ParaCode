#[derive(PartialEq, Debug, Clone)]
pub struct SourceLocation {
    pub filename: String,
    pub col: i32,
    pub row: i32,
}
impl SourceLocation {
    pub fn new(filename: String, col: i32, row: i32) -> SourceLocation {
        return SourceLocation {
            filename: filename,
            col: col,
            row: row,
        };
    }

    pub fn col_row(&self) -> (i32, i32) {
        return (self.col, self.row);
    }
}
