cd "${0%/*}"
cd ..

build_dir="target"
binary_dir="build"
build_configuration="debug"


rm -rf "$binary_dir/"
mkdir "$binary_dir/"
cargo build

# TODO: Handle this better
mv "$build_dir/$build_configuration/paracode" "$binary_dir/ParaCode"
# mv "$build_dir/$build_configuration/paracode.exe" "$binary_dir/ParaCode.exe"
