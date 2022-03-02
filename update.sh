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

rm ParaCode-rewrite/README.md
rm ParaCode-rewrite/CHANGELOG.md
rm ParaCode-rewrite/LICENSE
rm ParaCode-rewrite/.replit
mv ParaCode-rewrite/* .
mv ParaCode-rewrite/.* .
rm -rf ParaCode-rewrite
