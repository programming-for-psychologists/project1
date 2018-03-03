from psychopy import core, visual, prefs, event
import random
import sys
import copy
from useful_functions import *
from generateTrials import *


expName='recognition_memory_v1'
preFixationDelay = .75
postFixationDelay = .5
stimDuration = 1.0

postSoundDelayCorrect = 0.1
postSoundDelayIncorrect = 1.0


def initExperiment():

	while True:
		runTimeVarOrder = ['subjCode','seed','gender','whichSet']
		runTimeVars = getRunTimeVars({'subjCode':'memory_test', 'seed':10, 'gender':['Choose', 'male','female','other'], 'whichSet': ['Choose', '1', '2']},runTimeVarOrder,expName)
		if runTimeVars['subjCode']=='':
			popupError('Subject code is blank')				
		elif 'Choose' in runTimeVars.values():
			popupError('Need to choose a value from a dropdown box')
		else:
			try:
				study_outputFile = openOutputFile('data/'+runTimeVars['subjCode'],expName+'_study.csv')
				test_outputFile = openOutputFile('data/'+runTimeVars['subjCode'],expName+'_test.csv')
				if study_outputFile and test_outputFile: #files were able to be opened
					break
			except:
				popupError('Output file(s) could not be opened')

	generateStudyTrials(runTimeVars,runTimeVarOrder)
	generateTestTrials(runTimeVars,runTimeVarOrder)

	(study_header,study_trialInfo) = importTrialsWithHeader('trials/'+runTimeVars['subjCode']+'_study_trials.csv')
	(test_header,test_trialInfo) = importTrialsWithHeader('trials/'+runTimeVars['subjCode']+'_test_trials.csv')

	return (study_header, study_trialInfo, test_header, test_trialInfo, study_outputFile, test_outputFile)


def drawPlaceholder(lineColor="black", fillColor="white"):
	visual.Rect(win=win,size=(1040,1040), lineColor=lineColor, fillColor=fillColor, lineWidth=3).draw()

def showStudyTrial(curTrial,study_header,output_file,pics):
	win.flip()
	core.wait(preFixationDelay) 
	drawPlaceholder()
	fixationCross.draw()
	win.flip()
	core.wait(postFixationDelay)


	#insert study-trials related code here 

	isRight=1 #set this as needed
	RT = 0 #set this as needed
	
	#write study data to output file
	curTrial['header']=study_header
	trial_data=[curTrial[_] for _ in curTrial['header']] # add independent and runtime variables to what's written to the output file
	#write dependent variables
	trial_data.extend(
		(isRight,RT)
		)
	writeToFile(output_file,trial_data,writeNewLine=True)


def showTestTrial(curTrial,test_header,output_file,pics):

	#all the test trial code is here
	#use the rating scale object http://www.psychopy.org/api/visual/ratingscale.html
	#to render the 1-5 scale. Have people use keyboard (1-5) to respond rather than using the mouse (also an option for ratingscale)

	response=0 #set this as needed
	RT = 0 #set this as needed
	#include any other dependent variables

	#write test data to output file
	curTrial['header']=test_header
	trial_data=[curTrial[_] for _ in curTrial['header']] # add independent and runtime variables to what's written to the output file
	#write dependent variables
	trial_data.extend(
		(response,RT)
		)
	writeToFile(output_file,trial_data,writeNewLine=True)



if __name__ == '__main__':

	#there's a better way than passing all this info out of and into our functions. That better way is called using classes and objects.
	#we'll cover it in class soon
	(study_header, study_trialInfo, test_header, test_trialInfo, study_outputFile, test_outputFile) = initExperiment() #get runtime variables, create trial lists, etc.

	win = visual.Window(fullscr=True,allowGUI=False, color="gray", units='pix')
	pics =  loadFiles('stimuli/visual','.png','image', win=win) #can now access ImageStim objects as pics['filename']['stim']
	fixationCross = visual.TextStim(win=win,text="+",color="black",height=40)


	#show instructions etc.

	for i,curStudyTrial in enumerate(study_trialInfo):
		showStudyTrial(curStudyTrial,study_header,study_outputFile,pics)

	for i,curTestTrial in enumerate(test_trialInfo):
		showTestTrial(curTestTrial,test_header,test_outputFile,pics)

