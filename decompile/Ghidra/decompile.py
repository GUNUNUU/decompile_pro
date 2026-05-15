from __future__ import print_function
import json
import sys
import os
import string
#For Ghidra decompilation
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

#For IDA decompilation
from idautils import *
from idaapi import *
import ida_ida
import ida_auto
import ida_loader
import ida_hexrays
import ida_idp
import ida_entry
import ida_kernwin


class Decompilation():
    def __init__(self,func_info,process_order_dir,decompiled):
        self.func_info = func_info
        self.process_order_dir = process_order_dir
        self.decompiled = decompiled

    def ghidra_decompilation(self):
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


        function_info = "../func_info/func_info_speccpu/"+ori_bin

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
        
    
    
    def init_hexrays(self):
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
    

    def read_func_info(self,filename,func_info):
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
    

    def get_process_order(self,filename):
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
    

    def decompile_func(self,ea, outfile):
        ida_kernwin.msg("Decompiling at: %X..." % ea)
        cf = ida_hexrays.decompile(ea)
        if cf:
            ida_kernwin.msg("OK\n")
            outfile.write(str(cf) + "\n")
        else:
            ida_kernwin.msg("failed!\n")
            outfile.write("decompilation failure at %X!\n" % ea)
    

    def get_index(self, addr, process_order):

        for i in range(len(process_order)):
            if process_order[i] == int(str(addr),16):
                return i

        return -1
    
    def ida_decompilation(self):
        print("Waiting for autoanalysis...")
        ida_auto.auto_wait()
        if init_hexrays():
        
            idbpath = idc.get_idb_path()
            cpath = idbpath[:-4] + ".cpp"
            print(idbpath[:-4])
            needsDecompiledFunc = self.read_func_info(os.path.basename(idbpath[:-4]),func_info)
            process_order = self.get_process_order(os.path.basename(idbpath[:-4]))

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
                    self.decompile_func(funcea, outfile)


            print("All done, exiting.")
            ida_pro.qexit(0)
