rm -r build
mkdir build
cd build
cmake ../ && cmake --build . && ./ParaCode "$@"
cd ..