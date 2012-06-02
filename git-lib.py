#! /usr/bin/env python

import os
import glob
from subprocess import call
commits=[]

def main():
	getAllCommits()
	print getLastCommitMsg()
	
def getAllCommits():
	#x=call(["git","log",">","._tmp"])
	x=os.popen("git log")
	lines=x.readlines()
	for n in range(0,len(lines)):
		#print l[n].strip()
		if lines[n].strip().find("commit ")==0 and lines[n+1].strip().find("Author: ")==0 and lines[n+2].strip().find("Date: ")==0:
			cur_commit={}
			cur_commit["commit"]=lines[n].strip().split(" ")[1].strip()
			cur_commit["author"]=lines[n+1].strip().split(":")[1].strip()
			cur_commit["date"]=lines[n+2].strip().split(":")[1].strip()
			cur_commit["msg"]=lines[n+3].strip()
			x=4
			while len(lines) > (n+x) and lines[n+x].strip().find("commit ")!=0:
				cur_commit["msg"]+=lines[n+x].strip()
				print "appending",lines[n+x]
				x+=1
			commits.append(cur_commit)
			
	for c in commits:
		print c

def getLastCommitMsg():
	fin = open(".git/COMMIT_EDITMSG")
	lines=fin.readlines()
	return "".join(lines)
	
if __name__ == "__main__":
	main()
