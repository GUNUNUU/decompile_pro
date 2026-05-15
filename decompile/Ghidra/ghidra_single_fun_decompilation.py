#obtain the function signature from the decompiler
#obtain the variable type from the decompiler
#@yanlin 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 


#TODO Add User Code Here
import json
import sys
import os
import string
from ghidra.program.model.pcode import PcodeOp
#import ghidra.program.model.pcode.PcodeOpAST
import ghidra.program.database.DatabaseObject
from ghidra.program.model.lang.OperandType import SCALAR, REGISTER,INDIRECT
from collections import defaultdict
from ghidra.program.model.listing import VariableFilter
from  ghidra.program.model.listing import *
import ghidra.program.model.symbol.Symbol
from ghidra.program.model.pcode import *
from  ghidra.program.model.symbol import SymbolType;
import ghidra.program.database.symbol.NamespaceManager;
import ghidra.program.database.symbol.SymbolManager;
#from  ghidra.app.script.GhidraScript import *
from ghidra.app.script import GhidraScript
from ghidra.util.task import ConsoleTaskMonitor
import ghidra.framework.options.ToolOptions
import ghidra.app.script.GhidraState
import ghidra.framework.plugintool.util.OptionsService;




args = getScriptArgs()
response_dict = dict()

#if len(args) < 1:
	#print("usage: ./function-signature-analysis.py output_path")
	#sys.exit(0)

decompInterface = ghidra.app.decompiler.DecompInterface()
decompInterface.openProgram(currentProgram)

setAnalysisOption(currentProgram, "Decompiler Parameter ID", "true");
#setAnalysisOption(currentProgram, "Condense Filler Bytes", "true");
#setAnalysisOption(currentProgram, "Variadic Function Signature Override", "true");

bin_path = currentProgram.getExecutablePath()
ori_bin = os.path.basename(bin_path)
cwd = os.getcwd()

output_folder = os.path.join(cwd, 'ghidra-analysis-out/signature')
os.system("mkdir -p "+ output_folder)

output_path = os.path.join(output_folder, ori_bin+".txt")
#'/home/yanlin/ghidra-analysis-out/'+ori_bin+".txt"
decompiled_folder = os.path.join(cwd,'ghidra-analysis-out/decompiled')

os.system("mkdir -p " + decompiled_folder)

decompile_log = os.path.join(cwd,'ghidra-analysis-out/decompiled/decompile.log')

binary_folder = os.path.join(decompiled_folder,ori_bin)

os.system("mkdir -p " + binary_folder)


#decompile_path = os.path.join(decompiled_folder, ori_bin+".cpp")


function_info = "../func_info/func_info_github/"+ori_bin

needsDecompiledFunc = dict()


### get all functions that required to be decompiled  ###

with open(function_info,'r') as file:
	for line in file:
		line = line.split()

		func_addr = int(line[0],16)
		if func_addr < 0x400000:
			func_addr = 0x100000+func_addr
		#print(hex(func_addr))
		needsDecompiledFunc[func_addr] = line[1]


functionIterator = currentProgram.getFunctionManager().getFunctions(True)
decompiledFunc = list()
for function in functionIterator:
	indirect_call_info = defaultdict(list)


	#decompileResults = decompInterface.decompileFunction(
				#function, 30, monitor)

	setAnalysisOption(currentProgram, "Decompiler Parameter ID", "true");

	decompileResults = decompInterface.decompileFunction(
				function, 0, ConsoleTaskMonitor())
	
	fName = function.getName()
	address = function.getEntryPoint()

	if int(str(address),16) in needsDecompiledFunc:
		func_name = needsDecompiledFunc[int(str(address),16)]

		decompile_path = os.path.join(binary_folder,func_name)

		if not os.path.isfile(decompile_log):
			with open(decompile_log,'w') as file:
				file.write('\n')
		
		if not decompileResults.decompileCompleted():
			print('******* decompilation falied at '+ str(address))
			err = decompileResults.getErrorMessage()

			with open(decompile_log,'a') as file:
				#for line in all_decompiled_list:

				file.write('decompilation error at: '+ori_bin+'-'+func_name+" "+str(address)+"\n")
				file.write("decompilation falied: "+err+"\n")

		else:
			print('!!! decompilation ok at '+ str(address))
			decompiledFunction = decompileResults.getDecompiledFunction()
			decompiled = decompiledFunction.getSignature()
			
			all_decompiled = decompiledFunction.getC()

			#all_decompiled = all_decompiled.rstrip()
			#all_decompiled_list = all_decompiled.split("\n")
			#print >> fHandler, all_decompiled_list

			with open(decompile_path,'w') as file:
				#for line in all_decompiled_list:
				file.write(all_decompiled)
		






