#include "pch.h"

#include "ParaCode.h"
  
int main(int argc, char** argv)
{
    ParaCode paraCode = ParaCode();

    if (argc <= 1)
    {
        paraCode.repl();
        return 0;
    }

    // std::cout << "You have entered " << argc << " arguments:" << "\n";
  
    // for (int i = 0; i < argc; ++i)
    //     std::cout << argv[i] << "\n";

    std::string filename = argv[1];
    paraCode.evalFile(filename);
  
    return 0;
}
