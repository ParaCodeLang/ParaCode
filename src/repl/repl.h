#pragma once

#include "util.h"
#include "ParaCode.h"

#include <cpr/cpr.h>
#include "rapidjson/document.h"
#include <boost/filesystem.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/predicate.hpp>
#include <boost/regex.hpp>
replace_last_copy

#if !(defined(WIN32) || defined(_WIN32) || defined(__WIN32) && !defined(__CYGWIN__))
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <readline/readline.h>
#include <readline/history.h>
#endif

class Repl
{
public:
    static std::string REPL_FILENAME;
    std::map<std::string, std::tuple<std::string, std::string>> m_WalkthroughMessages;
    std::string m_WelcomeMessage = "";

    ParaCode* paraCode = nullptr;

    Repl() = default;
    Repl(ParaCode* paraCode)
    {
        this->paraCode = paraCode;

        // this->m_WalkthroughMessages = this->loadWalkthroughMessages();

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
            )"""", color + (Util::upper(paraCode->releaseStage) + " v" + paraCode->version) + LogColor::Default);

        // Version checking.
        // latestVersion = get("https://api.github.com/repos/DaRubyMiner360/ParaCode/releases/latest")
        cpr::Response r = cpr::Get(cpr::Url{"https://api.github.com/repos/DaRubyMiner360/ParaCode/releases/latest"});
        if (r.status_code == 200)
        {
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
        features and bug fixes.)"""", document["tag_name"].GetString(), document["published_at"].GetString()) + LogColor::Default;
        // features and bug fixes.)"""", document["tag_name"].GetString(), strptime(document["published_at"].GetString(), "%Y-%m-%dT%H:%M:%SZ").strftime('%A %b %d, %Y at %X')) + LogColor::Default;
            }
        }

        // TODO: Check if the user has used ParaCode
        std::string walkthrough = "";
        // for ()
        // '\n  '.join(map(lambda key: "{}--  {}".format(key.ljust(16), this->m_WalkthroughMessages[key][0]), this->m_WalkthroughMessages))
         this->m_WelcomeMessage += Util::format(R""""(
        

        Welcome to ParaCode Rewrite
        (codenamed Peaches).
        
        Let's get started!
        To learn more about ParaCode,
        type one of the following:

  %s
            )"""", walkthrough);
            // )"""".format('\n  '.join(map(lambda key: "{}--  {}".format(key.ljust(16), this->m_WalkthroughMessages[key][0]),this->.m_WalkthroughMessages)))
    }

    // void replImportDefaults() {
    //     // generate import nodes
    //     replImportNodes = [
    //         Parser.importFile(Parser, 'std/__core__.para'),
    //         Parser.importFile(Parser, 'std/__repl__.para')
    //     ]

    //     // eval asts
    //     this->evalLineAst(replImportNodes)
    // }

    void loop() {
        std::string lastInput = "";
        while (true) {
            this->acceptInput(lastInput);
        }
    }

    std::tuple<std::vector<std::string>, std::string> loadWalkthroughContent(std::string filename) {
        std::ifstream file(Util::format("./doc/%s", filename));
        int index = 0;
        std::vector<std::string> title;
        std::string content = "";
        for (std::string line; std::getline(file, line);) {
            if (index == 0) {
                title.push_back(Util::replaceAll(Util::trimCopy(line), "#", ""));
            }
            else {
                content += Util::trimCopy(line);
            }
            index++;
        }

        return std::make_tuple(title, content);
    }

    std::map<std::string, std::tuple<std::vector<std::string>, std::string>> loadWalkthroughMessages() {
        std::vector<std::string> f;
        for (const auto& p : boost::filesystem::directory_iterator("./doc")) {
            f.push_back(p.path().string());
        }
        std::sort(f.begin(), f.end());

        std::map<std::string, std::tuple<std::vector<std::string>, std::string>> walkthroughMessages;

        for (std::string filename : f) {
            if (boost::filesystem::exists(filename)) {
                boost::regex expr{"\\d\\d_([A-Za-z]*)\\.md"};
                boost::smatch x;
                boost::regex_search(filename, x, expr);
                std::string commandName = x[1];

                walkthroughMessages[commandName] = this->loadWalkthroughContent(filename);
            }
            else {
                std::cout << Util::format("Failed to load documentation file %s", filename) << std::endl;
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
        else if (this->m_WalkthroughMessages.count(trimmed) || (boost::algorithm::ends_with(trimmed, ".md") && this->m_WalkthroughMessages.count(boost::algorithm::replace_last_copy(trimmed, ".md", ""))) || (boost::algorithm::ends_with(trimmed, ".md/") && this->m_WalkthroughMessages.count(boost::algorithm::replace_last_copy(trimmed, ".md/", ""))))
            std::cout << this->m_WalkthroughMessages[trimmed][1].replace('```\n', '').replace('```javascript\n', '').replace('```js\n', '').replace('```typescript\n', '').replace('```ts\n', '').replace('```shell\n', '').replace('```bash\n', '').replace('`', '') << std::endl;
            return;
        }
    }
};

std::string Repl::REPL_FILENAME = "<repl>";
