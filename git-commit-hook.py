#! /usr/bin/env python

import os
import datetime
import json
from subprocess import call
commits=[]
fields=["tid","task","createdOn","createdBy","state","priority"]

# Return the current git user
def getGitUser():
	return "Matthias Lee"

def main():
	# Grabs the latest commit and then sees if there is a matching task
	lastCommit = getLastCommitMsg()
	tasks = getTasks()
	liveTasks = open(".tigger","w")
	completedTasks = open(".tigger_completed","a")
	for t in tasks:
		print t['task'].lower()
		if lastCommit["msg"].lower().find(t['task'].lower()) >= 0:
			print "completed:",t,datetime.datetime.now()
			print '{"completed":"'+str(datetime.datetime.now())+'","task":"'+t['task']+'"}\n'
			t["closed"]=str(datetime.datetime.now())
			t["closedBy"]=getGitUser()
			t["state"]="completed"
			#completedTasks.write('{"completed":"'+str(datetime.datetime.now())+'","task":"'+t+'"}\n')
			print json.dumps(t)
			liveTasks.write(json.dumps(t)+"\n")
		else:
			liveTasks.write(json.dumps(t)+"\n")
			
	liveTasks.close()
	completedTasks.close()

# Parse and Validate JSON
def parseJson(t_json):
	missingFields=""
	if t_json.strip() != "":
		try:
			# Parse Json, the verify
			jsonBits = json.loads(t_json.strip())
			
			valid=True
			# Check whether all required fields are present
			for f in fields:
				if f not in jsonBits:
					valid=False
					missingFields+=f+" "
			if valid:
				return jsonBits
			else:
				print "Missing JSON fields:",missingFields
		except:
			print "Error: invalid json entry. Skipping:",t_json.strip()
	else:
		# Something went wrong returning blank
		return ""

def getTasks():
	taskFile = open(".tigger", "r")
	tasks=[]
	for task in taskFile.readlines():
		jsonBits = parseJson(task)
		if jsonBits != "" and jsonBits != None:
			print "here:",type(jsonBits),jsonBits
			tasks.append(jsonBits)
			
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
