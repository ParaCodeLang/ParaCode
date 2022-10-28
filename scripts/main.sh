cd "${0%/*}"
cd ..

# sh scripts/build.sh
# echo "" && echo ""

# cd build/
# ./ParaCode "$@"
# cd ..

test=true
cargo test -- "$@" || exit
if [ "$test" = true ] ; then
    exit
else
    clear && cargo run -- "$@"
fi
