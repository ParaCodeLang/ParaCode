#pragma once

#include "util.h"
#include "ParaCode.h"
#include "error.h"
#include "interpreter/interpreter.h"
#include "lexer.h"

#include <cpr/cpr.h>
#include "rapidjson/document.h"
#include <boost/filesystem.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/join.hpp>
#include <boost/algorithm/string/predicate.hpp>
#include <boost/regex.hpp>

#include <iomanip>
#include <signal.h>

#if !(defined(WIN32) || defined(_WIN32) || defined(__WIN32) && !defined(__CYGWIN__))
#include <unistd.h>
#include <readline/readline.h>
#include <readline/history.h>
#endif

class Repl {
public:
    static std::string REPL_FILENAME;
    std::map<std::string, std::tuple<std::string, std::string>> m_WalkthroughMessages;
    std::string m_WelcomeMessage = "";

    ParaCode* paraCode = nullptr;

    Repl() = default;
    Repl(ParaCode* paraCode) {
        this->m_WalkthroughMessages = this->loadWalkthroughMessages();
        
        std::string color = LogColor::Default;
        if (paraCode->releaseStage == "alpha")
            color = "\033[95m";
        else if (paraCode->releaseStage == "beta")
            color = "\033[34m";
        else if (paraCode->releaseStage == "development")
            color = "\033[96m";
        else if (paraCode->releaseStage == "stable")
            color = "\033[92m";
        this->m_WelcomeMessage = Util::format(R""""(
            ----- P a r a C o d e -----
                %s
            )"""", (color + (Util::upper(paraCode->releaseStage) + " v" + paraCode->version) + LogColor::Default).c_str());

        // Version checking.
        // latestVersion = get("https://api.github.com/repos/DaRubyMiner360/ParaCode/releases/latest")
        cpr::Response r = cpr::Get(cpr::Url{"https://api.github.com/repos/DaRubyMiner360/ParaCode/releases/latest"});
        if (r.status_code == 200) {
            rapidjson::Document document;
            document.Parse(r.text.c_str());
            
            if (!document.HasMember("tag_name") || Util::versionCompare(document["tag_name"].GetString(), paraCode->version) < 0) {
                // Using unstable and/or development/beta version
                this->m_WelcomeMessage += LogColor::Warning + R""""(
        You are using a possibly unstable
        version! If something doesn't work
        correctly, that is probably why.)"""" + LogColor::Default;
            }
            else if (Util::versionCompare(document["tag_name"].GetString(), paraCode->version) > 0) {
                // Update available
                this->m_WelcomeMessage += LogColor::Warning + Util::format(R""""(
        Version %s is available to update
        to! It was released on %s.
        Download it from GitHub for new
        features and bug fixes.)"""", std::string(document["tag_name"].GetString()).c_str(), std::string(document["published_at"].GetString()).c_str()) + LogColor::Default;
        // features and bug fixes.)"""", document["tag_name"].GetString(), strptime(document["published_at"].GetString(), "%Y-%m-%dT%H:%M:%SZ").strftime("%A %b %d, %Y at %X")) + LogColor::Default;
            }
        }

        // TODO: Check if the user has used ParaCode
        std::string walkthrough = "";
        // "\n  ".join(map(lambda key: "{}--  {}".format(key.ljust(16), this->m_WalkthroughMessages[key][0]), this->m_WalkthroughMessages))
        std::vector<std::string> walkthroughs;
        for (auto const& pair : this->m_WalkthroughMessages) {
            walkthroughs.push_back(Util::format("%s--  %s", Util::ljustCopy(pair.first, 16).c_str(), std::get<0>(pair.second).c_str()));
        }
        this->m_WelcomeMessage += Util::format(R""""(
        

        Welcome to ParaCode Rewrite
        (codenamed Peaches).
        
        Let's get started!
        To learn more about ParaCode,
        type one of the following:

  %s
            )"""", boost::algorithm::join(walkthroughs, "\n  ").c_str());
            // )"""", walkthrough);
            // )"""".format("\n  ".join(map(lambda key: "{}--  {}".format(key.ljust(16), this->m_WalkthroughMessages[key][0]),this->.m_WalkthroughMessages)))

        this->paraCode = paraCode;
        // this->interpreter = Interpreter(SourceLocation(Repl::REPL_FILENAME));
        
        std::cout << this->m_WelcomeMessage << std::endl;

        this->replImportDefaults();

        signal(SIGINT, this->atExit);
    }

    static void atExit(int signal) {
        std::cout << "\nExiting..." << std::endl;
        std::exit(0);
    }

    void replImportDefaults() {
        // // generate import nodes
        // replImportNodes = [
        //     Parser.importFile(Parser, "std/__core__.para"),
        //     Parser.importFile(Parser, "std/__repl__.para")
        // ]

        // // eval asts
        // this->evalLineAst(replImportNodes)
    }

    void loop() {
        std::string lastInput = "";
        while (true) {
            this->acceptInput(lastInput);
        }
    }

    std::tuple<std::string, std::string> loadWalkthroughContent(std::string filename) {
        std::ifstream file(filename);
        int index = 0;
        std::string title;
        std::string content = "";
        std::string line;
        while (std::getline(file, line)) {
            if (index == 0) {
                title = Util::replaceAll(Util::trimCopy(line), "#", "");
            }
            else if (index > 1) {
                if (index > 2) {
                    content += "\n";
                }
                content += Util::trimCopy(line);
            }
            index++;
        }

        return std::make_tuple(title, content);
    }

    std::map<std::string, std::tuple<std::string, std::string>> loadWalkthroughMessages() {
        std::vector<std::string> f;
        for (const auto& p : boost::filesystem::directory_iterator(boost::filesystem::current_path() / "doc")) {
            f.push_back(p.path().string());
        }
        std::sort(f.begin(), f.end());

        std::map<std::string, std::tuple<std::string, std::string>> walkthroughMessages;

        for (std::string filename : f) {
            if (boost::filesystem::exists(filename)) {
                boost::regex expr{"\\d\\d_([A-Za-z]*)\\.md"};
                boost::smatch x;
                boost::regex_search(filename, x, expr);
                std::string commandName = x[1];

                walkthroughMessages[commandName] = this->loadWalkthroughContent(filename);
            }
            else {
                std::cout << Util::format("Failed to load documentation file %s", filename.c_str()) << std::endl;
            }
        }

        return walkthroughMessages;
    }

    void acceptInput(std::string& lastInput) {
#if defined(WIN32) || defined(_WIN32) || defined(__WIN32) && !defined(__CYGWIN__)
        std::string line = "";
        std::cout << ">>> ";
        std::getline(std::cin, line);
#else
        std::string line = readline(">>> ");
        if (line != "" && line != lastInput) {
            add_history(line.c_str());
            lastInput = line;
        }
#endif

        line = std::string(line);
        std::string trimmed = Util::trimCopy(line);

        // boost::filesystem::is_regular_file
        // boost::algorithm::ends_with
        if (boost::filesystem::is_regular_file(trimmed) && (boost::algorithm::ends_with(trimmed, ".para") || boost::algorithm::ends_with(trimmed, ".paracode"))) {
            this->paraCode->evalFile(trimmed);
            return;
        }
        else if (this->m_WalkthroughMessages.count(trimmed) || (boost::algorithm::ends_with(trimmed, ".md") && this->m_WalkthroughMessages.count(boost::algorithm::replace_last_copy(trimmed, ".md", ""))) || (boost::algorithm::ends_with(trimmed, ".md/") && this->m_WalkthroughMessages.count(boost::algorithm::replace_last_copy(trimmed, ".md/", "")))) {
            // Visual Studio Code syntax highlighting is whack.
            std::string str = boost::algorithm::replace_all_copy(boost::algorithm::replace_all_copy(std::get<1>(this->m_WalkthroughMessages[trimmed]), "```\n", ""), "```javascript\n", "");
            str = boost::algorithm::replace_all_copy(boost::algorithm::replace_all_copy(boost::algorithm::replace_all_copy(boost::algorithm::replace_all_copy(boost::algorithm::replace_all_copy(boost::algorithm::replace_all_copy(str, "```js\n", ""), "```typescript\n", ""), "```ts\n", ""), "```shell\n", ""), "```bash\n", ""), "`", "");
            std::cout << str << std::endl;
            return;
        }
        else if (trimmed == "doc" || trimmed == "docs" || trimmed == "documentation" || trimmed == "documentations" || trimmed == "walkthrough" || trimmed == "walkthroughs") {
            std::vector<std::string> walkthroughs;
            for (auto const& pair : this->m_WalkthroughMessages) {
                walkthroughs.push_back(Util::format("%s--  %s", Util::ljustCopy(pair.first, 16).c_str(), std::get<0>(pair.second).c_str()));
            }

            std::cout << Util::format(R""""(
  %s)"""", boost::algorithm::join(walkthroughs, "\n  ").c_str());
            return;
        }

        std::tuple<int, int, int, std::string> counts = this->countContinuationTokens(line);
        int braceCounter = std::get<0>(counts);
        int bracketCounter = std::get<1>(counts);
        int parenCounter = std::get<2>(counts);
        std::string commentType = std::get<3>(counts);

        while (braceCounter > 0 || bracketCounter > 0 || parenCounter > 0 || commentType != "") {
#if defined(WIN32) || defined(_WIN32) || defined(__WIN32) && !defined(__CYGWIN__)
            std::string nextLine = "";
            std::cout << "... ";
            std::getline(std::cin, nextLine);
#else
            std::string nextLine = readline("... ");
            if (nextLine != "" && nextLine != lastInput) {
                add_history(nextLine.c_str());
                lastInput = nextLine;
            }
#endif
            
            line += nextLine + "\n";
            counts = this->countContinuationTokens(line);
            braceCounter = std::get<0>(counts);
            bracketCounter = std::get<1>(counts);
            parenCounter = std::get<2>(counts);
            commentType = std::get<3>(counts);
        }

        // (lineAst, errorList) = this->parseLine(line);

        // // for node in lineAst:
        // //     AstPrinter().printAst(node)

        // if (errorList.errors.length > 0) {
        //     errorList.printErrors();
        //     return;
        // }

        // this->evalLineAst(lineAst);
    }

    // void evalLineAst(lineAst) {
    //     lastValue = nullptr
    //     lastNode = nullptr

    //     for (node : lineAst):
    //         lastNode = node;
    //         try {
    //             last_value = this->interpreter.visit(node);
    //         }
    //         catch InterpreterError {
    //             this->interpreter.errorList.clear_errors();
    //             continue;
    //         }

    //     if (lastValue != nullptr) {
    //         objStr = obj_to_string(this->interpreter, lastNode, lastValue)
    //         std::cout << LogColor::Info << objStr << LogColor::Default << std::endl;
    //     }
    // }

    // def parseLine(std::string line):
    //     Lexer lexer = Lexer(line, SourceLocation(Repl::REPL_FILENAME));
    //     tokens = lexer.lex();

    //     Parser parser = Parser(tokens, lexer.sourceLocation);

    //     return (parser.parse(), parser.errorList);

    std::tuple<int, int, int, std::string> countContinuationTokens(std::string line) {
        int braceCounter = 0;
        int bracketCounter = 0;
        int parenCounter = 0;

        std::string startedCommentChar = "";
        std::string commentType = "";

        for (auto& ch : line) {
            if (ch == '/' && commentType == "") {
                if (startedCommentChar != "/") {
                    startedCommentChar = "/";
                }
                else {
                    startedCommentChar = "";
                    commentType = "slash_slash";
                }
            }
            else if (ch == '*' && startedCommentChar == "/") {
                startedCommentChar = "";
                commentType = "slash_asterisk";
            }
            else if (ch == '#' && commentType == "" && startedCommentChar != "#") {
                startedCommentChar = "#";
                commentType = "hashtag";
            }
            else if (ch == '*' && startedCommentChar == "#") {
                startedCommentChar = "";
                commentType = "hashtag_asterisk";
            }
            else if (ch == '*' && startedCommentChar == "") {
                startedCommentChar = "*";
            }
            else if (ch == '/' && startedCommentChar == "*" && commentType == "slash_asterisk") {
                startedCommentChar = "";
                commentType = "";
            }
            else if (ch == '#' && startedCommentChar == "*" && commentType == "hashtag_asterisk") {
                startedCommentChar = "";
                commentType = "";
            }

            else if (ch == '{' && commentType == "") {
                braceCounter += 1;
            }
            else if (ch == '}' && commentType == "") {
                braceCounter -= 1;
            }
            else if (ch == '(' && commentType == "") {
                parenCounter += 1;
            }
            else if (ch == ')' && commentType == "") {
                parenCounter -= 1;
            }
            else if (ch == '[' && commentType == "") {
                bracketCounter += 1;
            }
            else if (ch == ']' && commentType == "") {
                bracketCounter -= 1;
            }
        }

        if (commentType == "slash_slash" || commentType == "hashtag") {
            commentType = "";
        }

        return std::make_tuple(braceCounter, bracketCounter, parenCounter, commentType);
    }
};

std::string Repl::REPL_FILENAME = "<repl>";
