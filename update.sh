rm -f doc
rm -f examples
rm -f interpreter
rm -f parse
rm -f repl
rm -f std
rm installDependencies.py
rm lexer.py
rm ParaCodeInstaller.iss
rm shell.py
rm shellTemplate.py
rm util.py
rm main.go
rm PCPM
rm update.sh

wget "http://github.com/DaRubyMiner360/ParaCode/archive/rewrite.zip" -O temp.zip
unzip temp.zip
rm temp.zip

rm ParaCode-rewrite/.replit
mv ParaCode-rewrite/* .
mv ParaCode-rewrite/.* .
rmdir -rf ParaCode-rewrite




# rm doc/*
# rmdir doc
# rmdir examples/__pycache__/*
# rm examples/__pycache__/*
# rmdir examples/__pycache__
# rmdir examples/*
# rm examples/*
# rmdir examples
# rmdir interpreter/env/builtin/__pycache__/*
# rm interpreter/env/builtin/__pycache__/*
# rmdir interpreter/env/builtin/__pycache__
# rmdir interpreter/env/builtin/*
# rm interpreter/env/builtin/*
# rmdir interpreter/env/builtin
# rmdir interpreter/env/__pycache__/*
# rm interpreter/env/__pycache__/*
# rmdir interpreter/env/__pycache__
# rmdir interpreter/env/*
# rm interpreter/env/*
# rmdir interpreter/env
# rmdir interpreter/typing/__pycache__/*
# rm interpreter/typing/__pycache__/*
# rmdir interpreter/typing/__pycache__
# rmdir interpreter/typing/*
# rm interpreter/typing/*
# rmdir interpreter/typing
# rmdir interpreter/__pycache__/*
# rm interpreter/__pycache__/*
# rmdir interpreter/__pycache__
# rmdir interpreter/*
# rm interpreter/*
# rmdir interpreter
# rmdir parse/__pycache__/*
# rm parse/__pycache__/*
# rmdir parse/__pycache__
# rmdir parse/*
# rm parse/*
# rmdir parse
# rmdir repl/__pycache__/*
# rm repl/__pycache__/*
# rmdir repl/__pycache__
# rmdir repl/*
# rm repl/*
# rmdir repl
# rmdir std/experimental/*
# rm std/experimental/*
# rmdir std/experimental
# rmdir std/io/*
# rm std/io/*
# rmdir std/io
# rmdir std/math/*
# rm std/math/*
# rmdir std/math
# rmdir std/types/math/matrix/*
# rm std/types/math/matrix/*
# rmdir std/types/math/matrix
# rmdir std/types/math/vectors/*
# rm std/types/math/vectors/*
# rmdir std/types/math/vectors
# rmdir std/types/math/*
# rm std/types/math/*
# rmdir std/types/math
# rmdir std/types/tk/*
# rm std/types/tk/*
# rmdir std/types/tk
# rmdir std/types/*
# rm std/types/*
# rmdir std/types
# rmdir std/util/*
# rm std/util/*
# rmdir std/util
# rmdir std/*
# rm std/*
# rmdir std
# rm installDependencies.py
# rm lexer.py
# rm ParaCodeInstaller.iss
# rm shell.py
# rm shellTemplate.py
# rm util.py
# rm main.go
# rm PCPM
# rm update.sh

# wget "http://github.com/DaRubyMiner360/ParaCode/archive/rewrite.zip" -O temp.zip
# unzip temp.zip
# rm temp.zip

# rm ParaCode-rewrite/.replit
# mv ParaCode-rewrite/* .
# mv ParaCode-rewrite/.* .
# rm ParaCode-rewrite/WIP/discord/core/*
# rmdir ParaCode-rewrite/WIP/discord/core/*
# rmdir ParaCode-rewrite/WIP/discord/core
# rm ParaCode-rewrite/WIP/discord/*
# rmdir ParaCode-rewrite/WIP/discord/*
# rmdir ParaCode-rewrite/WIP/discord
# rm ParaCode-rewrite/__pycache__/*
# rmdir ParaCode-rewrite/__pycache__/*
# rmdir ParaCode-rewrite/__pycache__
# rm ParaCode-rewrite/*
# rmdir ParaCode-rewrite/*
# rmdir ParaCode-rewrite
