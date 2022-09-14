cd "${0%/*}"
cd ..

#sh scripts/build.sh

dir="/usr/bin/"

rm -rf ParaCode/ 2>/dev/null
rm -f ParaCode.deb 2>/dev/null
mkdir -p "ParaCode/$dir"
cp -r std/ "ParaCode/$dir"
cp -r doc/ "ParaCode/$dir"
cp -r examples/ "ParaCode/$dir"
cp build/ParaCode "ParaCode/$dir" 2>/dev/null

cd ParaCode/

version="$(./ParaCode --version 2>/dev/null || echo "3.0.0")"

mkdir DEBIAN/
cd DEBIAN/

cat > control << EOF
Package: ParaCode
Version: $version
Maintainer: DaRubyMiner360
Architecture: all
Description: The ParaCode programming language.
EOF

cd ../../

dpkg-deb --build ParaCode


mkdir packages
mv ParaCode.deb packages/
