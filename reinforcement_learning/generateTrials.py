import random
from useful_functions import *
import numpy as np
import pandas as pd


def assign_key_to_stimuli(stimuli,keys,max_keys_per_stim, min_keys_per_stim):
	while True:
		stimulus_to_key = {stim:random.choice(keys) for stim in stimuli} 
		occurrences = [stimulus_to_key.values().count(curKey) for curKey in keys]
		if min(occurrences) == min_keys_per_stim and max(occurrences)<=max_keys_per_stim:
			return stimulus_to_key

def shuffleSlices(data,start,end):
	return random.sample(data[start:end],end-start)


def generateTrials(runTimeVars,runTimeVarOrder):
	try:
		random.seed(runTimeVars['seed']) #set random seed
	except:
		print 'make sure to set the random seed'


	stim_info = pd.read_csv("trial_info.csv",index_col=False)

	blocks = [3, 3, 4, 6]
	block_to_key_info = {3:[2,0], 4:[2,1], 6:[2,2]}
	keys = ['z','x','c']
	stims_in_blocks = []
	max_iterations = 15
	max_trials_per_block = list(np.array(blocks)*max_iterations)

	stim_names = list(stim_info['name'])
	random.shuffle(stim_names)
	stims_in_blocks=[]
	for curBlock in blocks:
		stims_in_blocks.append([stim_names.pop() for i in range(curBlock)])
		#now we know which Droodles we'll have in each block


	trialData=[]
	for blockNum,curBlock in enumerate(blocks):
		trialData.append([])
		trialData[blockNum] = assign_key_to_stimuli(stims_in_blocks[blockNum],keys,block_to_key_info[curBlock][0],block_to_key_info[curBlock][1])


	trialsFile = open('trials/'+runTimeVars['subjCode']+'_trials.csv','w')

	data=[]
	curBlockNum=0
	for blockNum,curBlock in enumerate(trialData):
		data.append([])
		curTrialIndex=0
		for curIter in range(max_iterations):
			for stimName,key in curBlock.items():
				data[curBlockNum].append([])
				for curRuntimeVar in runTimeVarOrder:
					data[blockNum][curTrialIndex].append(runTimeVars[curRuntimeVar])
				data[blockNum][curTrialIndex].extend(map(str,(blockNum, stimName, key, stim_info[stim_info.name==stimName]['description'].values[0], len(trialData[blockNum]))))
				curTrialIndex+=1
		curBlockNum+=1

	#proper way of shuffling, but doing any version of this will be too complicated for people. Could be made more concise...
	#shuffled_data=[]
	# #the 'three' blocks
	# shuffle_in_multiple_of = 15
	# begin_at = 0
	# end_at = begin_at+max_iterations * 3 * blocks.count(3)
	# for start in range(begin_at,end_at,shuffle_in_multiple_of):
	# 	shuffled_data.extend(shuffleSlices(data,start,start+shuffle_in_multiple_of))

	# #the 'four' blocks
	# shuffle_in_multiple_of = 20
	# begin_at = 90
	# end_at = begin_at+max_iterations * 4 * blocks.count(4)
	# for start in range(begin_at,end_at,shuffle_in_multiple_of):
	# 	shuffled_data.extend(shuffleSlices(data,start,start+shuffle_in_multiple_of))

	# #the 'six' blocks
	# shuffle_in_multiple_of = 15
	# begin_at = 150
	# end_at = begin_at+max_iterations * 6 * blocks.count(6)
	# for start in range(begin_at,end_at,shuffle_in_multiple_of):
	# 	shuffled_data.extend(shuffleSlices(data,start,start+shuffle_in_multiple_of))

	header = runTimeVarOrder
	header.extend(('block', 'stim', 'key', 'description', 'numStimsInBlock', 'trialIndex'))
	writeToFile(trialsFile,[colName for colName in runTimeVarOrder]) 


	for curBlock in data:
		random.shuffle(curBlock)
		for trialIndex,curTrial in enumerate(curBlock):
			curTrial.append(trialIndex)
			writeToFile(trialsFile,curTrial)



if __name__ == '__main__':
	#this is what's executed if you run generateTrials.py from the terminal
	generateTrials({'subjCode':'testSubj1', 'seed':'6', 'gender':'male','condition':'noDescr'}, ['subjCode', 'seed', 'condition'])	
	generateTrials({'subjCode':'testSubj2', 'seed':'6', 'gender':'male','condition':'wDescr'}, ['subjCode', 'seed', 'condition'])	
	generateTrials({'subjCode':'testSubj3', 'seed':'7', 'gender':'male','condition':'noDescr'}, ['subjCode', 'seed', 'condition'])	
	generateTrials({'subjCode':'testSubj4', 'seed':'7', 'gender':'male','condition':'wDescr'}, ['subjCode', 'seed', 'condition'])	
	
