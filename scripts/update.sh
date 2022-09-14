cd "${0%/*}"
cd ..

rm -f src
rm -f vendor
rm -f build
rm -f doc
rm -f examples
rm -f std
rm -f scripts

wget "http://github.com/ParaCodeLang/ParaCode/archive/rewrite-cpp.zip" -O temp.zip
unzip temp.zip
rm temp.zip

rm ParaCode-rewrite-cpp/README.md
rm ParaCode-rewrite-cpp/CHANGELOG.md
rm ParaCode-rewrite-cpp/LICENSE
rm ParaCode-rewrite-cpp/.replit
mv ParaCode-rewrite-cpp/* .
mv ParaCode-rewrite-cpp/.* .
rm -rf ParaCode-rewrite-cpp
