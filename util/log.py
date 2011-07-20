'''
Function write(message, errlevel = 3):
	message is what you want to log, 
	and level as its loglevel

Variable loglevel:
	only errlevel>=loglevel will be write
	to the logfile. Default value is 3

Variable screenlevel:
	if errlevel>=screenlevel then the message
	will be printed to the screen(stderr).
	Default value is 3

Variable logfile:
	filename to store log
'''
from time import asctime
import sys
loglevel = 3
screenlevel = 3
logfile = "/var/log/rejudger.log"

def write(msg, errlevel = 3):
	global loglevel
	global screenlevel
	global logfile
	msg = '[' + asctime() + '] ' + str(msg)
	if (loglevel <= errlevel):
		logfile = open(logfile, "a")
		logfile.writelines([msg])
		logfile.close()
	if (screenlevel <= errlevel):
		sys.stderr.writelines([msg])

