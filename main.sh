if [ -d "build" ]; then
    # rm -rf _build
    # mv build _build
    rm -rf build
fi

mkdir build
# if [ -d "_build" ]; then
#     cp _build/_deps build/_deps
#     cp _build/boost_1_78_0 build/boost_1_78_0
#     cp _build/boost_1_78_0_GNU_5_4_0 build/boost_1_78_0_GNU_5_4_0
#     cp _build/boost_1_78_0.tar.bz2 build/boost_1_78_0.tar.bz2
#     cp _build/boost_1_78_0.tar.bz2 build/boost_1_78_0.tar.bz2
#     cp _build/vendor build/vendor
#     # cp _build/CMakeFiles/boost_* build/CMakeFiles
# fi
cp -r doc build/doc
cp -r examples build/examples
cp -r std build/std
cd build

if [ "$debug" = true ] ; then
    cmake -DCMAKE_BUILD_TYPE=Debug ../ && cmake --build . && gdb ./ParaCode "$@"
else
    cmake ../ && cmake --build . && ./ParaCode "$@"
fi
cd ..
