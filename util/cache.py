#!/usr/bin/env python2
#coding=utf-8
'''
Cache for testdata.

Function getdata(problem_id, timestamp, casecount):
	This will check the timestamp of current cache file
	and server data. And return the dataset of problem.
	[
		{"infile" : "", "outfile" : ""},
		{"infile" : "", "outfile" : ""},
		...
	]

Variable cachedir.
'''

import os, log
import urllib

cachedir = '/var/cache/rejudger'
prefix = ''

def __update(problem_id, timestamp, casecount):
	global prefix
	global cachedir
	for index in range(1, casecount + 1):
		filename = "/".join((cachedir, str(problem_id), str(index) + ".in"))
		url = "/".join((prefix, str(problem_id), "data", str(index) + ".in"))
		print url
		urllib.urlretrieve(url, filename)
		filename = "/".join((cachedir, str(problem_id), str(index) + ".out"))
		url = "/".join((prefix, str(problem_id), "data", str(index) + ".out"))
		urllib.urlretrieve(url, filename)
	
	f = open("/".join((cachedir, str(problem_id), "timestamp")), "w")
	f.write(str(timestamp))
	f.close()
	pass

def __get_current_timestamp(problem_id):
	filename = "/".join((cachedir, str(problem_id), "timestamp"))
	import os
	if (os.path.exists(filename) == False):
		return 0
	f = open(filename, "r")
	if (f == None):
		return 0
	else:
		timestamp = int(f.read())
		f.close()
		return timestamp
	pass

def getdata(problem_id, timestamp, casecount):
	global cachedir
	current_dir = "/".join((cachedir, str(problem_id)))
	if (os.path.exists(current_dir) == False):
		os.mkdir(current_dir)
	if (__get_current_timestamp(problem_id) < timestamp):
		__update(problem_id, timestamp, casecount)
	ret = []
	for index in range(1, casecount + 1):
		fileprefix = "/".join((cachedir, str(problem_id), str(index)))
		ret.append({"infile" : fileprefix + ".in", "outfile" : fileprefix + ".out"})

	return ret
	pass

