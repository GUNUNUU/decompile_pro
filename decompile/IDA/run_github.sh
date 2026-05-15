mkdir -p ../IDADecompiled/github/original/clang/O0
mkdir -p ../IDADecompiled/github/original/clang/O1
mkdir -p ../IDADecompiled/github/original/clang/O2
mkdir -p ../IDADecompiled/github/original/clang/O3
mkdir -p ../IDADecompiled/github/original/gcc/O0
mkdir -p ../IDADecompiled/github/original/gcc/O1
mkdir -p ../IDADecompiled/github/original/gcc/O2
mkdir -p ../IDADecompiled/github/original/gcc/O3


# python batch_decompile_ida_no_order.py ../binary/github/original_binary/clang/O0/
# cp -r ../decompiled/* ../IDADecompiled/github/original/clang/O0
# rm -r ../decompiled/*
# cp ./decompile.log ../IDADecompiled/github/original/clang/O0
# rm -f ./decompile.log

# python batch_decompile_ida_no_order.py ../binary/github/original_binary/clang/O1/
# cp -r ../decompiled/* ../IDADecompiled/github/original/clang/O1
# rm -r ../decompiled/*
# cp ./decompile.log ../IDADecompiled/github/original/clang/O1
# rm -f ./decompile.log

# python batch_decompile_ida_no_order.py ../binary/github/original_binary/clang/O2/
# cp -r ../decompiled/* ../IDADecompiled/github/original/clang/O2
# rm -r ../decompiled/*
# cp ./decompile.log ../IDADecompiled/github/original/clang/O2
# rm -f ./decompile.log

# python batch_decompile_ida_no_order.py ../binary/github/original_binary/clang/O3/
# cp -r ../decompiled/* ../IDADecompiled/github/original/clang/O3
# rm -r ../decompiled/*
# cp ./decompile.log ../IDADecompiled/github/original/clang/O3
# rm -f ./decompile.log

python batch_decompile_ida_no_order.py ../binary/github/original_binary/gcc/O0/
cp -r ../decompiled/* ../IDADecompiled/github/original/gcc/O0
rm -r ../decompiled/*
cp ./decompile.log ../IDADecompiled/github/original/gcc/O0
rm -f ./decompile.log

python batch_decompile_ida_no_order.py ../binary/github/original_binary/gcc/O1/
cp -r ../decompiled/* ../IDADecompiled/github/original/gcc/O1
rm -r ../decompiled/*
cp ./decompile.log ../IDADecompiled/github/original/gcc/O1
rm -f ./decompile.log

python batch_decompile_ida_no_order.py ../binary/github/original_binary/gcc/O2/
cp -r ../decompiled/* ../IDADecompiled/github/original/gcc/O2
rm -r ../decompiled/*
cp ./decompile.log ../IDADecompiled/github/original/gcc/O2
rm -f ./decompile.log

python batch_decompile_ida_no_order.py ../binary/github/original_binary/gcc/O3/
cp -r ../decompiled/* ../IDADecompiled/github/original/gcc/O3
rm -r ../decompiled/*
cp ./decompile.log ../IDADecompiled/github/original/gcc/O3
rm -f ./decompile.log