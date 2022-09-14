cd "${0%/*}"
cd ..

sh scripts/build.sh
cd build

if [ "$debug" = true ] ; then
    gdb ./ParaCode "$@"
else
    ./ParaCode "$@"
fi

cd ..
