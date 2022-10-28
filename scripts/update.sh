cd "${0%/*}"
cd ..

rm -f src
rm -f build
rm -f doc
rm -f examples
rm -f std
rm -f scripts

wget "http://github.com/ParaCodeLang/ParaCode/archive/rewrite-rust.zip" -O temp.zip
unzip temp.zip
rm temp.zip

rm ParaCode-rewrite-rust/README.md
rm ParaCode-rewrite-rust/CHANGELOG.md
rm ParaCode-rewrite-rust/LICENSE
rm ParaCode-rewrite-rust/.replit
mv ParaCode-rewrite-rust/* .
mv ParaCode-rewrite-rust/.* .
rm -rf ParaCode-rewrite-rust
