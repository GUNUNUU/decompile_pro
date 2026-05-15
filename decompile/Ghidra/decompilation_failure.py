import sys
import os 



class DecompilationFaliure():
	def __init__(self):
		self.count = ['coreutils','diffutils','findutils']
		pass
	

	def decompilationFaliure(self,decompile_log,decompiler)
		failure_dict = dict()
		failure_dict_ida = dict()
		with open(decompile_log) as f:
			for line in f:
				if decompiler == 'ida':

					if "has been successfully loaded into the database" in line:
						binary = line[5:len(line)-len("has been successfully loaded into the database")]
						#print(binary)
						#if 'binutils' in binary or 'coreutils' in binary or 'inetutils' in binary:

					if "ida_hexrays.DecompilationFailure: Decompilation failed:" in line:
						#print(line)
						temp = line.split(':')
						failure_type = temp[-1]
						#if failure_type not in failure_dict:
						if not ('diffutils' in binary or 'coreutils' in binary or 'findutils' in binary):
							if failure_type not in failure_dict:
								failure_dict[failure_type] = 1
							else:
								failure_dict[failure_type] += 1
						failure_dict_ida[binary]=failure_type
						#else:
							#failure_dictbinary[binary][failure_type] += 1
				elif decompiler == 'ghidra':
					if "Low-level Error: " in line:
						print(line)
						temp = line.split(':')
						failure_type = temp[-1]
						if failure_type not in failure_dict:
							failure_dict[failure_type] = 1
						else:
							failure_dict[failure_type] += 1

		print(failure_dict)