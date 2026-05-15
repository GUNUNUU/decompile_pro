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

func_info = r"../func_info/func_info_speccpu"
process_order_dir = r"../ida_process_order/ida_process_order_speccpu"
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
			#needsDecompiledFunc.append(func_addr)
			needsDecompiledFunc[func_addr] = funcName

	return needsDecompiledFunc


def get_process_order(filename):
	file_path=os.path.join(process_order_dir,filename)
	process_order = list()

	with open(file_path,'r') as file:
		for line in file:
			line = line.rstrip()
			line = line.split(" ")
			func_addr = int(line[0],16)
			#print(hex(func_addr))
			process_order.append(func_addr)

	return process_order

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

def decompile_func(ea, outfile):
	ida_kernwin.msg("Decompiling at: %X..." % ea)
	cf = ida_hexrays.decompile(ea)
	if cf:
		ida_kernwin.msg("OK\n")
		outfile.write(str(cf) + "\n")
	else:
		ida_kernwin.msg("failed!\n")
		outfile.write("decompilation failure at %X!\n" % ea)

def get_index(addr, process_order):

	for i in range(len(process_order)):
		if process_order[i] == int(str(addr),16):
			return i

	return -1



def main():
	print("Waiting for autoanalysis...")
	ida_auto.auto_wait()
	if init_hexrays():
	
		idbpath = idc.get_idb_path()
		cpath = idbpath[:-4] + ".cpp"
		print(idbpath[:-4])
		needsDecompiledFunc = read_func_info(os.path.basename(idbpath[:-4]))
		process_order = get_process_order(os.path.basename(idbpath[:-4]))

		#get_func_1_ea()
		process_func_ea_inOrder = [0]*len(process_order)
		#with open(cpath, "w") as outfile:
			#print("writing results to '%s'..." % cpath)
		for funcea in Functions():
			#functionName = GetFunctionName(funcea)
			functionStart = "0x%08x"%funcea
			print("func start:", functionStart)

			functionName=''
			if int(str(functionStart),16) in needsDecompiledFunc:
				functionName = needsDecompiledFunc[int(str(functionStart),16)]

			index = get_index(functionStart,process_order)

			if index != -1:

				process_func_ea_inOrder[index] = (funcea, functionName)

		#with open(cpath, "w") as outfile:
			#print("writing results to '%s'..." % cpath)
		decompiled_result = os.path.join(decompiled, os.path.basename(idbpath[:-4]))
		os.system("mkdir -p " + decompiled_result)
		for i in range(len(process_func_ea_inOrder)):
			(funcea,functionName) = process_func_ea_inOrder[i]
			outfileName = os.path.join(decompiled_result, functionName)
			with open(outfileName, 'w') as outfile:
				decompile_func(funcea, outfile)


		print("All done, exiting.")
		ida_pro.qexit(0)



if __name__ == '__main__':

	main()