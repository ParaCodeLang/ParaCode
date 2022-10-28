cd "${0%/*}"
cd ..

cargo test -- "$@"