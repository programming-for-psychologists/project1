import random
import pandas as pd
from useful_functions import *

def has_sequential(lst):
	lst = sorted(lst)
	for elt in zip(lst,lst[1:]):
		if elt[1]-elt[0]==1:
			return True
	return False


def generateStudyTrials(runTimeVars,runTimeVarOrder):

	try:
		random.seed(runTimeVars['seed']) #set random seed
	except:
		print 'make sure to set the random seed'

	n_nonspecial_repeats = 20
	num_study_trials = 180 #180 total - 20 repeats - 52 special-stims = 108 non_special stims

	columns = runTimeVarOrder[:]
	columns.extend(['trialNum', 'category', 'isRepeat', 'imageFile', 'relationship'])

	studyFile = open('trials/'+runTimeVars['subjCode']+'_study_trials.csv','w')
	writeToFile(studyFile,[colName for colName in columns]) #prints the headers. make sure to extend this with column names you're adding


	# Based on this participant's whichSet,
	# decide which special stims they get
	# in the study phase.
	stim_info = pd.read_csv('stimulus_info.csv')
	special_stims = list(stim_info['category'+runTimeVars['whichSet']])
	

	all_special_stims = [line.rstrip() for line in open('special_stims.txt')]
	all_stims = [line.rstrip() for line in open('all_stims.txt')]
	nonspecial_stims = [stim for stim in all_stims if stim not in all_special_stims]

	num_non_special_stims = num_study_trials - n_nonspecial_repeats - len(special_stims)
	nonspecial_stims = random.sample(nonspecial_stims,num_non_special_stims) #get a sub-sample of the non-special stims, else too many
	study_stims = special_stims + random.sample(nonspecial_stims,num_non_special_stims)
	random.shuffle(study_stims)


	repeat_stims = random.sample(nonspecial_stims, n_nonspecial_repeats)
	repeat_indices = [study_stims.index(repeat_stim) for repeat_stim in repeat_stims]
	while min(repeat_indices)<5 or has_sequential(repeat_indices):
		repeat_stims = random.sample(nonspecial_stims, n_nonspecial_repeats)
		repeat_indices = [study_stims.index(repeat_stim) for repeat_stim in repeat_stims]

	study_with_repeats = study_stims[:]
	offset=0
	for i in range(160):
		if study_stims[i] in repeat_stims:
			study_with_repeats.insert(i+offset,study_stims[i])
			offset+=1

	trials = []
	for trial_num,study_item in enumerate(study_with_repeats):
		trial = runTimeVars.copy()
		trial['trialNum'] = trial_num
		trial['category'] = study_item
		trial['imageFile'] = study_item+'_'+runTimeVars['imageVersion']
		if study_with_repeats[trial_num-1] in repeat_stims and study_with_repeats[trial_num] in repeat_stims:
			trial['isRepeat'] = 1
		else:
			trial['isRepeat'] = 0
		try:
			trial['relationship'] = stim_info[stim_info['category'+runTimeVars['whichSet']]==study_item]['relationship'].values[0]
		except:
			trial['relationship'] = 'exemplar'

		trials.append(trial)

	#write data to file
	for trial in trials:
		ordered_trial_row = [trial[name] for name in columns]
		writeToFile(studyFile, ordered_trial_row)

	return (study_with_repeats, repeat_stims)


def generateTestTrials(runTimeVars,runTimeVarOrder,study_with_repeats,repeat_stims):
	def oppositeSet(num):
		if int(num)==1:
			return '2'
		elif int(num)==2:
			return '1'

	num_test_trials = 100
	try:
		random.seed(runTimeVars['seed']) #set random seed
	except:
		print 'make sure to set the random seed'

	columns = runTimeVarOrder[:]
	columns.extend(['trialNum', 'category', 'imageFile', 'trialType', 'relationship'])

	testFile = open('trials/'+runTimeVars['subjCode']+'_test_trials.csv','w')
	writeToFile(testFile,[colName for colName in columns]) #prints the headers. make sure to extend this with column names you're adding

	# Based on this participant's whichSet,
	# decide which special stims they get
	# in the test phase.
	stim_info = pd.read_csv('stimulus_info.csv')
	stim_info = pd.read_csv('stimulus_info.csv')
	special_stims_study = list(stim_info['category'+runTimeVars['whichSet']])
	special_stims_test = list(stim_info['category'+oppositeSet(runTimeVars['whichSet'])])
	special_stims = dict(zip(special_stims_study, special_stims_test)) #make a dictionary for easy lookup, e.g., palm-tree:palm-hang

	num_old_trials = 50
	old_stims = set(study_with_repeats).difference(repeat_stims).difference(special_stims_study) #repeated stims aren't tested
	old_stims = random.sample(old_stims,num_old_trials)

	exemplar_stims = set(study_with_repeats).difference(repeat_stims).difference(old_stims)
	exemplar_stims = random.sample(exemplar_stims,24)

	test_stims = old_stims+exemplar_stims+special_stims_test
	random.shuffle(test_stims)

	trials = []
	for trial_num,test_item in enumerate(test_stims):
		trial = runTimeVars.copy()

		trial['trialNum'] = trial_num
		trial['category'] = test_item

		if test_item in old_stims:
			trial['trialType'] = 'old'
			trial['imageFile'] = trial['category']+'_'+runTimeVars['imageVersion']
		elif test_item in exemplar_stims:
			trial['trialType'] = 'new'
			trial['imageFile'] = test_item+'_'+oppositeSet(runTimeVars['imageVersion'])
		else:
			# special stim, in test phase, keep imageVersion what it was in study phase
			trial['trialType'] = 'new'
			trial['imageFile'] = trial['category']+'_'+runTimeVars['imageVersion']

		try:
			trial['relationship'] = stim_info[stim_info['category'+runTimeVars['whichSet']]==test_item]['relationship'].values[0]
		except:
			trial['relationship'] = 'exemplar'
		trials.append(trial)


	for trial in trials:
		ordered_trial_row = [trial[name] for name in columns]
		writeToFile(testFile, ordered_trial_row)


if __name__ == '__main__':
	#this is what's executed if you run generateTrials.py from the terminal
	(study_with_repeats, repeat_stims) = generateStudyTrials({'subjCode':'testSubj1', 'seed':'9', 'whichSet':'1', 'imageVersion': '1'}, ['subjCode', 'seed', 'whichSet', 'imageVersion'])
	generateTestTrials({'subjCode':'testSubj1', 'seed':'9', 'whichSet':'1', 'imageVersion': '1'}, ['subjCode', 'seed', 'whichSet', 'imageVersion'],study_with_repeats, repeat_stims)

	(study_with_repeats, repeat_stims) = generateStudyTrials({'subjCode':'testSubj2', 'seed':'9', 'whichSet':'2', 'imageVersion': '1'}, ['subjCode', 'seed', 'whichSet', 'imageVersion'])
	generateTestTrials({'subjCode':'testSubj2', 'seed':'9', 'whichSet':'2', 'imageVersion': '1'}, ['subjCode', 'seed', 'whichSet', 'imageVersion'],study_with_repeats, repeat_stims)

	(study_with_repeats, repeat_stims) = generateStudyTrials({'subjCode':'testSubj3', 'seed':'9', 'whichSet':'2', 'imageVersion': '2'}, ['subjCode', 'seed', 'whichSet', 'imageVersion'])
	generateTestTrials({'subjCode':'testSubj3', 'seed':'9', 'whichSet':'2', 'imageVersion': '2'}, ['subjCode', 'seed', 'whichSet', 'imageVersion'],study_with_repeats, repeat_stims)


