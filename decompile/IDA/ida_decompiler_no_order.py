# 
# cmd: <path_to_ida.exe> -A -OIDAPython:1;<path_to_idapy_test.py> <path_to_program>
#                                       ^ 1 is important, this script will be executed after hexrays is loaded.
from __future__ import print_function
from idautils import *
from idaapi import *


import ida_ida
import ida_auto
import ida_loader
import ida_hexrays
import ida_idp
import ida_entry
import ida_kernwin

func_info = r"../func_info/func_info_github"
decompiled = r"../decompiled"


def init_hexrays():
	ALL_DECOMPILERS = {
	ida_idp.PLFM_386: "hexrays",
	ida_idp.PLFM_ARM: "hexarm",
	ida_idp.PLFM_PPC: "hexppc",
	ida_idp.PLFM_MIPS: "hexmips",
	}
	cpu = ida_idp.ph.id
	decompiler = ALL_DECOMPILERS.get(cpu, None)
	if not decompiler:
		print("No known decompilers for architecture with ID: %d" % ida_idp.ph.id)
		return False
	if ida_ida.inf_is_64bit():
		if cpu == ida_idp.PLFM_386:
			decompiler = "hexx64"
		else:
			decompiler += "64"
	if ida_loader.load_plugin(decompiler) and ida_hexrays.init_hexrays_plugin():
		return True
	else:
		print('Couldn\'t load or initialize decompiler: "%s"' % decompiler)
		return False



def read_func_info(filename):
	file_path=os.path.join(func_info,filename)
	needsDecompiledFunc = dict()
	with open(file_path,'r') as file:
		for line in file:
			line = line.rstrip()
			line = line.split(" ")
			func_addr = int(line[0],16)
			funcName = line[1]
			#print(hex(func_addr))
			needsDecompiledFunc[func_addr] = funcName

	return needsDecompiledFunc


def get_func_ea():
	global func_1_ea
	#ea = BeginEA()
	#for funcea in Functions(SegStart(ea), SegEnd(ea)):
	for funcea in Functions():
		functionName = GetFunctionName(funcea)
		functionStart = "0x%08x"%funcea
		functionEnd = "0x%08x"%FindFuncEnd(funcea)
		print("func name:", functionName)
		print("func start:", functionStart)
		print("func end:", functionEnd)
		#if functionName == 'func_1':  # only decompile one function
			#func_1_ea = funcea

# yanlin
# def decompile_func(ea, outfile):
# 	ida_kernwin.msg("Decompiling at: %X..." % ea)
# 	cf = ida_hexrays.decompile(ea)
# 	print("cf output:",cf)
# 	if cf:
# 		ida_kernwin.msg("OK\n")
# 		outfile.write(str(cf) + "\n")
# 	else:
# 		ida_kernwin.msg("failed!\n")
# 		outfile.write("decompilation failure at %X!\n" % ea)

# maliha
def decompile_func(ea, outfile):
    try:
        ida_kernwin.msg("Decompiling at: %X..." % ea)
        cf = ida_hexrays.decompile(ea)
        # print("cf output:", cf)
        if cf:
            ida_kernwin.msg("OK\n")
            outfile.write(str(cf) + "\n")
        else:
            ida_kernwin.msg("failed!\n")
            outfile.write("decompilation failure at %X!\n" % ea)
    except Exception as e:
        ida_kernwin.msg("Exception: {}\n".format(e))

def main():
	print("Waiting for autoanalysis...")
	ida_auto.auto_wait()
	if init_hexrays():
		idbpath = idc.get_idb_path()
		cpath = idbpath[:-4] + ".cpp"
		print(idbpath[:-4])	
		needsDecompiledFunc = read_func_info(os.path.basename(idbpath[:-4]))	
		#get_func_1_ea()
		decompiled_result = os.path.join(decompiled, os.path.basename(idbpath[:-4]))
		os.system("mkdir -p " + decompiled_result)

		#with open(cpath, "w") as outfile:
			#print("writing results to '%s'..."  cpath)
		for funcea in Functions():
	 		# functionName = GetFunctionName(funcea)
			functionStart = "0x%08x"%funcea
			#functionEnd = "0x%08x"%FindFuncEnd(funcea)
			# print("func name:", functionName)
			print("func start:", functionStart)
			#print("func end:", functionEnd)
			#if functionName == 'func_1':  # only decompile one function
				#func_1_ea = funcea
			functionName=''
			if int(str(functionStart),16) in needsDecompiledFunc:
				if needsDecompiledFunc[int(str(functionStart),16)]:
					functionName = needsDecompiledFunc[int(str(functionStart),16)]
					outfileName = os.path.join(decompiled_result, functionName)
					with open(outfileName, 'w') as outfile:
						decompile_func(funcea, outfile)

	#if ida_kernwin.cvar.batch:
	print("All done, exiting.")
	ida_pro.qexit(0)
	


if __name__ == '__main__':
	main()