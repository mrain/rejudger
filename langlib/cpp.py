#coding=utf-8
'''
C++ Module for rejudger
'''

import subprocess, os, re

RUNNER = "/home/mrain/source/oj_acm/judger/judger-run"

compile_message = ''

def __run(args = None, trust = False, timelimit = None, memorylimit = None, infile = None, outfile = None, errfile = None, fsize = None):
	'''Using RUNNER to exec args.'''
	cmd = [RUNNER]
	if trust:
		cmd.append("--trust")
	if timelimit != None:
		cmd.extend(["--time", str(timelimit)])
	if memorylimit != None:
		cmd.extend(["--memory", str(memorylimit)])
	if infile != None:
		cmd.extend(["--input", str(infile)])
	if outfile != None:
		cmd.extend(["--output", str(outfile)])
	if errfile != None:
		cmd.extend(["--stderr", str(errfile)])
	if fsize != None:
		cmd.extend(["--fsize", str(fsize)])
	cmd.append(args)
	cmd = " ".join(cmd)
#	print cmd
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
	return p

def compile(name, code):
	f = open("%s.cpp" % (name), "w");
	f.write(code);
	f.close();

	compile_pattern = "g++ %s.cpp -o %s -O2 -Wall -static -DONLINE_JUDGE" % (name, name)
	
	com_msg_file = "%s_com_msg" % name
	com_err_file = "%s_com_err" % name
	process = __run(args = compile_pattern, trust = True, timelimit = 30 * 1000, outfile = com_msg_file, errfile = com_err_file, fsize = 50 * 1024 * 1024, memorylimit = 1 * 1024 * 1024 * 1024)
	(result, stderr) = process.communicate()

	try:
		global compile_message
		f = file(com_msg_file, "r")
		compile_message = f.read()
		f.close()
		f = file(com_err_file, "r")
		compile_message += f.read()
		f.close()
		compile_message = compile_message.replace(name, "test")
	except IOError as e:
		return False

	if "NORMAL" not in result:
		return False

	if (os.path.exists(name) == False):
		return False

	return True

def execute(name, timelimit, memorylimit, outputlimit, infile, outfile):
	process = __run(
			args = "./" + name,
			timelimit = timelimit,
			memorylimit = memorylimit,
			fsize = outputlimit,
			infile = infile,
			outfile = outfile,
			errfile = "/dev/null"
			)
	time = 0.0
	memory = 0.0
	(res_string, stderr) = process.communicate()
	if "NORMAL_EXIT" in res_string:
		p = re.compile("\d+.\d+")
		time, memory = p.findall(res_string)
		memory = int(memory) / 1024
		time = int(float(time) * 1000.0)
		verdict = 1
	else:
		verdict = 9
		if "SIGNALED" in res_string:
			verdict = 6
		if "Memory Limit Exceeded" in res_string:
			verdict = 4
		if "Time Limit Exceeded" in res_string:
			verdict = 3
		if "Output Limit Exceeded" in res_string:
			verdict = 7
		if "Runtime Error" in res_string:
			verdict = 6
		if "RESTRICTED_SYSCALL" in res_string:
			verdict = 6
		if "NON-ZERO_RETURN_CODE" in res_string:
			verdict = 6
	
	return {"time" : time, "memory" : memory, "verdict" : verdict}
