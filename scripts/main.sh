cd "${0%/*}"
cd ..

# sh scripts/build.sh
# echo "" && echo ""

# cd build/
# ./ParaCode "$@"
# cd ..

run=false
cargo test -- "$@" || exit
if [ "$run" = false ] ; then
    exit
else
    clear && cargo run -- "$@"
fi
