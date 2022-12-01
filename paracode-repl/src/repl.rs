use std::path::Path;
use std::collections::HashMap;

use rustyline::error::ReadlineError;
use rustyline::Editor;

use paracode::paracode::ParaCode;
use paracode::parse::source_location::SourceLocation;
use paracode::lexer::Lexer;
use paracode::utils::LogColor;

pub struct Repl {
    paracode: ParaCode,
    welcome_message: String,
    
    last_input: String,
    rl: Editor::<()>,

    walkthrough_messages: HashMap<String, (String, String)>,
}

impl Repl {
    pub fn filename() -> String {
        return "<repl>".to_string();
    }

    // Needs load_walkthrough_messages
    pub fn new(paracode: ParaCode) -> Repl {
        let walkthrough_messages = HashMap::<String, (String, String)>::new();//self.load_walkthrough_messages();
        
        let mut color = LogColor::default();
        if paracode.release_stage() == "alpha" {
            color = "\x1b[95m".to_string();
        }
        else if paracode.release_stage() == "beta" {
            color = "\x1b[34m".to_string();
        }
        else if paracode.release_stage() == "development" {
            color = "\x1b[96m".to_string();
        }
        else if paracode.release_stage() == "stable" {
            color = "\x1b[92m".to_string();
        }
        let welcome_message = format!("
            ----- P a r a C o d e -----
                {}
            ", format!("{}{}{}", color, format!("{} v{}", paracode.release_stage().to_uppercase(), paracode.version()), LogColor::default()));

        // TODO: Version checking.

        // TODO: Add the actual welcome message to welcome_message
        
        let mut repl = Repl {
            paracode: paracode,
            // interpreter: Interpreter::new(SourceLocation::new(Repl::filename())),
            welcome_message: welcome_message,
            
            last_input: "".to_string(),
            rl: Editor::<()>::new().unwrap(),

            walkthrough_messages: walkthrough_messages
        };

        println!("{}", repl.welcome_message);

        repl.repl_import_defaults();

        return repl;
    }

    fn at_exit(&self) {
        println!("\nExiting...");
        quit::with_code(0);
    }

    pub fn repl_import_defaults(&mut self) {
    }

    pub fn run(&mut self) {
        loop {
            _ = self.accept_input();
        }
    }

    // load_walkthrough_content

    // load_walkthrough_messages

    pub fn accept_input(&mut self) -> Result<(), String> {
        let line = match self.rl.readline(">>> ") {
            Ok(line) => line,
            Err(ReadlineError::Interrupted) => {
                self.at_exit();
                "".to_string()
            },
            Err(ReadlineError::Eof) => {
                self.at_exit();
                "".to_string()
            },
            Err(err) => {
                println!("\nError: {:?}", err);
                quit::with_code(1);
            }
        };
        if line.as_str() != "" && line != self.last_input {
            self.rl.add_history_entry(line.as_str());
            self.last_input = line.as_str().to_string();
        }

        let trimmed = line.trim();
        if Path::new(trimmed).is_file() && (trimmed.ends_with(".para") || trimmed.ends_with(".paracode")) {
            // self.paracode.eval_file(trimmed);

            return Ok(());
        }
        else if self.walkthrough_messages.contains_key(trimmed) || (trimmed.ends_with(".md") && self.walkthrough_messages.contains_key(&trimmed.replace(".md", ""))) || (trimmed.ends_with(".md/") && self.walkthrough_messages.contains_key(&trimmed.replace(".md/", ""))) {
            // println!(self.walkthrough_messages[trimmed][1].replace("```\n", "").replace("```javascript\n", "").replace('```js\n', '').replace('```typescript\n', '').replace('```ts\n', '').replace('```shell\n', '').replace('```bash\n', '').replace('`', ''))

            return Ok(());
        }
        else if trimmed == "doc" || trimmed == "docs" || trimmed == "documentation" || trimmed == "documentations" || trimmed == "walkthrough" || trimmed == "walkthroughs" {
            let mut walkthroughs = vec![];
            for (key, value) in &self.walkthrough_messages {
                walkthroughs.push(format!("{}--  {}", format!("{: >16}", key), value.0));
            }
            println!("
  {}", walkthroughs.join("\n  "));

            return Ok(());
        }

        let (brace_counter, bracket_counter, paren_counter, comment_type) = self.count_continuation_tokens(&line);

        while brace_counter > 0 || bracket_counter > 0 || paren_counter > 0 || comment_type != "" {
            //
        }

        let (line_ast, error_list) = self.parse_line(line)?;

        //

        return Ok(());
        // todo!("Handle received input");
    }

    // eval_line_ast

    // Needs Parser
    pub fn parse_line(&self, line: String) -> Result<((), ()), String> {
        let mut lexer = Lexer::new(&line, SourceLocation::new(Repl::filename(), 1, 1));
        let tokens = lexer.lex()?;

        // let parser = Parser::new(tokens, lexer.source_location);

        // return Ok(parser.parse(), parser.error_list);
        return Ok(((), ()));
    }

    pub fn count_continuation_tokens(&self, line: &String) -> (i32, i32, i32, String) {
        let mut brace_counter = 0;
        let mut bracket_counter = 0;
        let mut paren_counter = 0;

        let mut started_comment_char = "";
        let mut comment_type = "";

        for ch in line.chars() {
            if ch == '/' && comment_type == "" {
                if started_comment_char != "/" {
                    started_comment_char = "/";
                }
                else {
                    started_comment_char = "";
                    comment_type = "slash_slash";
                }
            }
            else if ch == '*' && started_comment_char == "/" {
                started_comment_char = "";
                comment_type = "slash_asterisk";
            }
            else if ch == '#' && comment_type == "" && started_comment_char != "#" {
                started_comment_char = "#";
                comment_type = "hashtag";
            }
            else if ch == '*' && started_comment_char == "#" {
                started_comment_char = "";
                comment_type = "hashtag_asterisk";
            }
            else if ch == '*' && started_comment_char == "" {
                started_comment_char = "*";
            }
            else if ch == '/' && started_comment_char == "*" && comment_type == "slash_asterisk" {
                started_comment_char = "";
                comment_type = "";
            }
            else if ch == '#' && started_comment_char == "*" && comment_type == "hashtag_asterisk" {
                started_comment_char = "";
                comment_type = "";
            }

            else if ch == '{' && comment_type == "" {
                brace_counter += 1;
            }
            else if ch == '}' && comment_type == "" {
                brace_counter -= 1;
            }
            else if ch == '(' && comment_type == "" {
                paren_counter += 1;
            }
            else if ch == ')' && comment_type == "" {
                paren_counter -= 1;
            }
            else if ch == '[' && comment_type == "" {
                bracket_counter += 1;
            }
            else if ch == ']' && comment_type == "" {
                bracket_counter -= 1;
            }
        }

        if comment_type == "slash_slash" || comment_type == "hashtag" {
            comment_type = "";
        }

        return (brace_counter, bracket_counter, paren_counter, comment_type.to_string());
    }
}
