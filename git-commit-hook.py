#! /usr/bin/env python

import os
import datetime
from subprocess import call
commits=[]

def main():
	# Grabs the latest commit and then sees if there is a matching task
	lastCommit = getLastCommitMsg()
	tasks = getTasks()
	liveTasks = open(".tigger","w")
	completedTasks = open(".tigger_completed","a")
	for t in tasks:
		if lastCommit["msg"].lower().find(t.lower()) >= 0:
			print "completed:",t,datetime.datetime.now()
			completedTasks.write('{"completed":"'+str(datetime.datetime.now())+'","task":"'+t+'"}\n')
		else:
			liveTasks.write(t+"\n")
			
	liveTasks.close()
	completedTasks.close()

def getTasks():
	taskFile = open(".tigger", "r")
	tasks=[]
	for task in taskFile.readlines():
		if task.strip()!="":
			tasks.append(task.strip())
	return tasks

# Returns all git commits in a List of Dicts, 1 for each commit
def getAllCommits():
	x=os.popen("git log")
	lines=x.readlines()
	for n in range(0,len(lines)):
		# Check for the a complete commit then parse and put into Dict
		if lines[n].strip().find("commit ")==0 and lines[n+1].strip().find("Author: ")==0 and lines[n+2].strip().find("Date: ")==0:
			cur_commit={}
			cur_commit["commit"]=lines[n].strip().split(" ")[1].strip()
			cur_commit["author"]=lines[n+1].strip().split(":")[1].strip()
			cur_commit["date"]=lines[n+2].strip().split(":")[1].strip()
			cur_commit["msg"]=lines[n+3].strip()
			x=4
			# Grab multiline commit messages
			while len(lines) > (n+x) and lines[n+x].strip().find("commit ")!=0:
				cur_commit["msg"]+=lines[n+x].strip()
				x+=1
			# Build up list of commits
			commits.append(cur_commit)
			
	return commits

# Returns the most recent commit message by calling git log -1
def getLastCommitMsg():
	x=os.popen("git log -1")
	lines=x.readlines()
	for n in range(0,len(lines)):
		# Check for the a complete commit then parse and put into Dict
		if lines[n].strip().find("commit ")==0 and lines[n+1].strip().find("Author: ")==0 and lines[n+2].strip().find("Date: ")==0:
			cur_commit={}
			cur_commit["commit"]=lines[n].strip().split(" ")[1].strip()
			cur_commit["author"]=lines[n+1].strip().split(":")[1].strip()
			cur_commit["date"]=lines[n+2].strip().split(":")[1].strip()
			cur_commit["msg"]=lines[n+3].strip()
			x=4
			# Grab multiline commit messages
			while len(lines) > (n+x) and lines[n+x].strip().find("commit ")!=0:
				cur_commit["msg"]+=lines[n+x].strip()
				x+=1
			# Only returning the first one anyway
			return cur_commit
	
if __name__ == "__main__":
	main()
