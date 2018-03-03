import random
from useful_functions import *


def generateTrials(runTimeVars,runTimeVarOrder):
	"""
	Generate trials corresponding to 4 blocks The first should have 3 images, then another 3, then 4, and 6 for the last.
	You'll want to run people in "yoked pairs" such that subject 1 and 2 are set to the seed (and so will get the same exact trials
	 
	"""
	try:
		random.seed(runTimeVars['seed']) #set random seed
	except:
		print 'make sure to set the random seed'

	trialsFile = open('trials/'+runTimeVars['subjCode']+'_trials.csv','w')
	writeToFile(trialsFile,[colName for colName in runTimeVarOrder]) #prints the headers. make sure to extend this with column names you're adding

	for trial in range(10):
		writeToFile(trialsFile,['something']*len(runTimeVarOrder))



if __name__ == '__main__':
	#this is what's executed if you run generateTrials.py from the terminal
	generateTrials({'subjCode':'testSubj1', 'seed':'6', 'gender':'male','condition':'wDescr'}, ['subjCode', 'seed', 'condition'])	
	
