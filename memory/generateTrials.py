import random
from useful_functions import *


def generateStudyTrials(runTimeVars,runTimeVarOrder):
	try:
		random.seed(runTimeVars['seed']) #set random seed
	except:
		print 'make sure to set the random seed'

	studyFile = open('trials/'+runTimeVars['subjCode']+'_study_trials.csv','w')
	writeToFile(studyFile,[colName for colName in runTimeVarOrder]) #prints the headers. make sure to extend this with column names you're adding

	for trial in range(10):
		writeToFile(studyFile,['something']*len(runTimeVarOrder))


def generateTestTrials(runTimeVars,runTimeVarOrder):
	try:
		random.seed(runTimeVars['seed']) #set random seed
	except:
		print 'make sure to set the random seed'

	testFile = open('trials/'+runTimeVars['subjCode']+'_test_trials.csv','w')
	writeToFile(testFile,[colName for colName in runTimeVarOrder]) #prints the headers. make sure to extend this with column names you're adding

	for trial in range(10):
		writeToFile(testFile,['something']*len(runTimeVarOrder))


if __name__ == '__main__':
	#this is what's executed if you run generateTrials.py from the terminal
	generateStudyTrials({'subjCode':'testSubj1', 'seed':'6', 'gender':'male','whichSet':'1'}, ['subjCode', 'seed', 'whichSet'])	
	generateTestTrials({'subjCode':'testSubj1', 'seed':'6', 'gender':'male','whichSet':'1'}, ['subjCode', 'seed', 'whichSet'])	

