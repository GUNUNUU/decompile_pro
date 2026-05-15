mkdir -p ../IDADecompiled/SPECCPU/original/clang/O0
mkdir -p ../IDADecompiled/SPECCPU/original/clang/O1
mkdir -p ../IDADecompiled/SPECCPU/original/clang/O2
mkdir -p ../IDADecompiled/SPECCPU/original/clang/O3
mkdir -p ../IDADecompiled/SPECCPU/original/gcc/O0
mkdir -p ../IDADecompiled/SPECCPU/original/gcc/O1
mkdir -p ../IDADecompiled/SPECCPU/original/gcc/O2
mkdir -p ../IDADecompiled/SPECCPU/original/gcc/O3
# python batch_decompile_ida.py ../binary/SPECCPU2006/clang/O0/original_binary
# cp -r ../decompiled/* ../IDADecompiled/SPECCPU/original/clang/O0
# rm -r ../decompiled/*
# cp ./decompile.log ../IDADecompiled/SPECCPU/original/clang/O0
# rm -f ./decompile.log

# python batch_decompile_ida.py ../binary/SPECCPU2006/clang/O1/original_binary
# cp -r ../decompiled/* ../IDADecompiled/SPECCPU/original/clang/O1
# rm -r ../decompiled/*
# cp ./decompile.log ../IDADecompiled/SPECCPU/original/clang/O1
# rm -f ./decompile.log


# python batch_decompile_ida.py ../binary/SPECCPU2006/clang/O2/original_binary
# cp -r ../decompiled/* ../IDADecompiled/SPECCPU/original/clang/O2
# rm -r ../decompiled/*
# cp ./decompile.log ../IDADecompiled/SPECCPU/original/clang/O2
# rm -f ./decompile.log

# python batch_decompile_ida.py ../binary/SPECCPU2006/clang/O3/original_binary
# cp -r ../decompiled/* ../IDADecompiled/SPECCPU/original/clang/O3
# rm -r ../decompiled/*
# cp ./decompile.log ../IDADecompiled/SPECCPU/original/clang/O3
# rm -f ./decompile.log

#------------------------------------------------------------------
python batch_decompile_ida.py ../binary/SPECCPU2006/gcc/O0/original_binary
cp -r ../decompiled/* ../IDADecompiled/SPECCPU/original/gcc/O0
rm -r ../decompiled/*
cp ./decompile.log ../IDADecompiled/SPECCPU/original/gcc/O0
rm -f ./decompile.log

python batch_decompile_ida.py ../binary/SPECCPU2006/gcc/O1/original_binary
cp -r ../decompiled/* ../IDADecompiled/SPECCPU/original/gcc/O1
rm -r ../decompiled/*
cp ./decompile.log ../IDADecompiled/SPECCPU/original/gcc/O1
rm -f ./decompile.log

python batch_decompile_ida.py ../binary/SPECCPU2006/gcc/O2/original_binary
cp -r ../decompiled/* ../IDADecompiled/SPECCPU/original/gcc/O2
rm -r ../decompiled/*
cp ./decompile.log ../IDADecompiled/SPECCPU/original/gcc/O2
rm -f ./decompile.log

python batch_decompile_ida.py ../binary/SPECCPU2006/gcc/O3/original_binary/
cp -r ../decompiled/* ../IDADecompiled/SPECCPU/original/gcc/O3
rm -r ../decompiled/*
cp ./decompile.log ../IDADecompiled/SPECCPU/original/gcc/O3
rm -f ./decompile.log