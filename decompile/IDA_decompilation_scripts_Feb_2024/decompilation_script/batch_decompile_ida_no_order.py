import os
import sys
#from subprocess import Popen, PIPE, getstatusoutput


process_dir = os.getcwd()

if __name__ == '__main__':
    binary_dir = sys.argv[1]
    #target_dir = sys.argv[2]
    #os.system("mkdir -p " + target_dir)

    for binary in os.listdir(binary_dir):
        # if binary.startswith('gcc'):  # git, redis*, 
            binary_path = os.path.join(binary_dir,binary)
            processing_path = os.path.join(process_dir,binary)
            print(binary)
            print(binary_path)
            print(processing_path)
            os.system('cp '+binary_path+" "+processing_path)
            cmd = r"/opt/idapro-7.7/idat64 -A  -OIDAPython:1 -Ldecompile.log -Sida_decompiler_no_order.py -c " + processing_path
            print(cmd)            
            os.system(cmd)            
            #cpp_path = os.path.join(process_dir, binary+".cpp ")
            #target_path=os.path.join(target_dir, binary+".cpp ")
            #os.system("cp " + cpp_path +" " + target_path)
            #os.system("del "+binary+".i64")
            os.system("rm -f "+ processing_path)
            os.system("rm -f "+binary+".*")
