#pragma once

#include "pch.h"

#include "util.h"

class ParaCode;

class Repl
{
public:
    static std::string REPL_FILENAME;
    std::vector<std::string> m_WalkthroughMessages;
    std::string m_WelcomeMessage = "";

    Repl() = default;
    Repl(ParaCode* paraCode)
    {
        // this->m_WalkthroughMessages = this->loadWalkthroughMessages();

        std::string color = LogColor.Default;
        if (paraCode->releaseStage == "alpha")
            color = "\033[95m";
        else if (paraCode->releaseStage == "beta")
            color = "\033[34m";
        else if (paraCode->releaseStage == "development")
            color = "\033[96m";
        else if (paraCode->releaseStage == "stable")
            color = "\033[92m";
        this->m_WelcomeMessage = std::format(R"
            ----- {} -----
                {}
            ", "P a r a C o d e", color + (paraCode->releaseStage.upper() + " v" + paraCode.version) + LogColor.Default);
    }
};

std::string Repl::REPL_FILENAME = "<repl>";
