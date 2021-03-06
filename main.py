#! /usr/bin/env python
# pyTigger
import optparse
import os
import shutil
import json
import datetime

postCommitHookPath="./git-commit-hook.py"
# todo: colored output?
#	http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python


# Asks the user a question and veryfies y/n by returning True or False
def confirmQuestion(Question):
	var=""
	while var != "y" and var != "n":
		var = raw_input(Question + " (y/n):" )
	if var == "y":
		return True
	else:
		return False

def initTigger(force):
	if os.path.exists("./.tigger") and force == False:
		print "It looks like tigger has already been initialized here."
		print "\tUse -f or --force to initilize anyway."
		exit()

	if os.path.isdir("./.git"):
		# We are in the clear, we found git and no previous tigger
		print "git found."
		if os.path.exists(".git/hooks/post-commit"):
			print "ERROR: .git/hooks/post-commit hook already exists"
			if confirmQuestion("Would you like to overwrite the existing hook?") == False:
				print "exiting.."
				exit()
		try:
			print "Installing postCommit hook.."
			shutil.copyfile(postCommitHookPath,".git/hooks/post-commit")
			# set permissions
			os.system("chmod 744 .git/hooks/post-commit")
			# todo: check permissions after setting
		except Exception as err:
			print err
			print "failed to copy post-commit hook from",postCommitHookPath,"to .git/hooks/post-commit"

		# Initialize files
		os.system("touch .tigger")
		os.system("touch .tigger_completed")
		print "Created .tigger & .tigger_complete"
		
		# Add to repo
		os.system("git add .tigger")
		os.system("git add .tigger_completed")
		print "Added .tigger & .tigger_complete to repo"		
		
	else:
		print "ERROR: no git-repo found. (looking for .git)"
		exit()
	print "Init done."

def listCompleted(todayOnly=False):
	if os.path.exists("./.tigger_completed") == False:
		print "It looks like .tigger_completed is missing."
		print "\tPerhaps you are in the wrong directory?"
		print "\tor you need to run --init to create a tigger instance."
		exit()
		
	tasksFile = open("./.tigger_completed","r")
	tasks = tasksFile.readlines()
	for n,t in enumerate(tasks):
		jt=""
		try:
			jt = json.loads(t.strip())
		except Exception as err:
			print err
			print "malformed line in .tigger_completed, line", n+1

		if todayOnly and jt!="":
			if "completed" in jt:
				# check for existance of "completed" and if dt is today
				dt=datetime.datetime.strptime(jt["completed"],"%Y-%m-%d %H:%M:%S.%f")
				if datetime.date.today()==dt.date():
					print jt
		elif jt!="":
			print jt

# todo: duplicate of listComplete?
def listTasks():
	if os.path.exists("./.tigger") == False:
		print "It looks like .tigger is missing."
		print "\tPerhaps you are in the wrong directory?"
		print "\tor you need to run --init to create a tigger instance."
		exit()
	tasksFile = open("./.tigger","r")
	tasks = tasksFile.readlines()
	for t in tasks:
		# todo: parse JSON
		print t.strip()
		
# Return a new(hopefully unique) Task ID
def getNewTID():
	return 1

# Return the current git user
def getGitUser():
	return "Matthias Lee"

def addTask(task):
	print "adding:",task
	if os.path.exists("./.tigger") == False:
		print "It looks like .tigger is missing."
		print "\tPerhaps you are in the wrong directory?"
		print "\tor you need to run --init to create a tigger instance."
		exit()
	liveTasks =  open(".tigger", "a")
	tid=getNewTID()
	createdOn=str(datetime.datetime.now())
	createdBy=getGitUser()
	state="new"
	newTiggerTask='{"tid":'+str(tid)+','
	newTiggerTask+='"task":"'+task+'",'
	newTiggerTask+='"createdOn":"'+createdOn+'",'
	newTiggerTask+='"createdBy":"'+createdBy+'",'
	newTiggerTask+='"state":"new",'
	newTiggerTask+='"priority":"normal"}\n'
	print newTiggerTask
	liveTasks.write(newTiggerTask)
	liveTasks.close()

if __name__ == "__main__":
	optparser = optparse.OptionParser()
	optparser.add_option("-i", "--init", action="store_true", dest="init_flag", default=False, help="Initialize a pyTigger")
	optparser.add_option("-n", "--new", dest="new_task", type="string", default=False, help="Create a new task")
	optparser.add_option("-l", "--tasks", action="store_true", dest="tasks_flag", default=False, help="List outstanding tasks")
	optparser.add_option("-t", "--tig", action="store_true", dest="tig_flag", default=False, help="Tigger")
	optparser.add_option("-c", "--completed", action="store_true", dest="comp_flag", default=False, help="List completed tasks")
	optparser.add_option("-d", "--delete", dest="del_task", type="string", default=False, help="Delete a task")
	optparser.add_option("-g", "--glory", action="store_true", dest="glory_flag", default=False, help="Bathe yourself in todays acomplishments")
	optparser.add_option("-f", "--force", action="store_true", dest="force_flag", default=False, help="List outstanding tasks")
	(opts,args) = optparser.parse_args()
	print "Options set:"
	print opts
	print args
	if opts.init_flag!=False or os.path.isdir("./.git")==False:
		print "initializing tigger..."
		initTigger(opts.force_flag)
	elif opts.new_task!=False:
		print "creating new task", opts.new_task
		addTask(opts.new_task)
	elif opts.del_task!=False:
		print "deleting task", opts.del_task
	elif opts.tig_flag!=False:
		print "lets tigger"
	elif opts.comp_flag!=False:
		print "list completed tasks"
		listCompleted()
	elif opts.tasks_flag!=False:
		print "list outstangind tasks"
		listTasks()
	elif opts.glory_flag!=False:
		print "Today's accomplishments"
		listCompleted(True)
	else:
		print "error no valid option selected, use -h for help"
		
