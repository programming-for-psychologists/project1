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
blankScreenDuration=.15


def initExperiment():

	while True:
		runTimeVarOrder = ['subjCode','seed','gender','whichSet', 'imageVersion']
		runTimeVars = getRunTimeVars({'subjCode':'memory_test', 'seed':10, 'gender':['Choose', 'male','female','other'], 'whichSet': ['Choose', '1', '2'], 'imageVersion': ['Choose', '1', '2']},runTimeVarOrder,expName)
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

	(study_with_repeats, repeat_stims) = generateStudyTrials(runTimeVars, runTimeVarOrder)
	generateTestTrials(runTimeVars, runTimeVarOrder, study_with_repeats, repeat_stims)

	(study_header,study_trialInfo) = importTrialsWithHeader('trials/'+runTimeVars['subjCode']+'_study_trials.csv')
	(test_header,test_trialInfo) = importTrialsWithHeader('trials/'+runTimeVars['subjCode']+'_test_trials.csv')

	return (study_header, study_trialInfo, test_header, test_trialInfo, study_outputFile, test_outputFile)


def drawPlaceholder(lineColor="black", fillColor="white"):
	visual.Rect(win=win,size=(1040,1040), lineColor=lineColor, fillColor=fillColor, lineWidth=3).draw()

def showInstructions(win):
	visual.TextStim(win=win,text="Instructions go here.",color="darkred",height=40).draw()
	win.flip()
	event.waitKeys()


def showStudyTrial(curTrial,study_header,output_file,pics):
	
	def showIncorrectFeedback():
		visual.TextStim(win=win,text="Missed Repeat",color="darkred", height=60,pos=(0,200)).draw()
		visual.TextStim(win=win,text="Please Pay Closer Attention",color="black", height=60,pos=(0,-50)).draw()
		win.flip()
		core.wait(1)


	response='NA'
	responseReceived=False
	RT='NA'

	drawPlaceholder()
	fixationCross.draw()
	win.flip()
	core.wait(postFixationDelay)

	drawPlaceholder()
	pics[curTrial['imageFile']]['stim'].draw()
	win.flip()
	responseTimer = core.Clock()
	while responseTimer.getTime()<stimDuration:
		if not responseReceived:
			response = event.getKeys(keyList=['space'])
			if response:
				responseReceived=True
				RT = responseTimer.getTime()
	

	drawPlaceholder()
	win.flip()
	while responseTimer.getTime()<blankScreenDuration+stimDuration:
		if not responseReceived:
			response = event.getKeys(keyList=['space'])
			if response:
				responseReceived=True
				RT = responseTimer.getTime()

	print 'RESPONDED', responseReceived, response, RT, responseTimer.getTime()

	if response!=['space'] and int(curTrial['isRepeat']):
		showIncorrectFeedback()

	isRight= int(response==['space'] and int(curTrial['isRepeat']) or response!=['space'] and not int(curTrial['isRepeat']))	

	if response != 'NA':
		RT *= 1000
	
	#write study data to output file
	curTrial['header']=study_header
	trial_data=[curTrial[_] for _ in curTrial['header']] # add independent and runtime variables to what's written to the output file
	#write dependent variables
	trial_data.extend(
		(isRight,RT)
		)
	writeToFile(output_file,trial_data,writeNewLine=True)


def showTestTrial(curTrial,test_header,output_file,pics):

	fixationCross.draw()
	win.flip()
	core.wait(preFixationDelay) 

	ratingScale = visual.RatingScale(win, textSize=0.7, textColor="black", lineColor='darkblue', \
		showAccept=False, choices=[1,2,3,4,5], respKeys=['1','2','3','4','5'], pos=(0,-320),noMouse=True, marker=visual.TextStim(win,text=""), singleClick=True)
	while ratingScale.noResponse:
		visual.TextStim(win=win, text="Have you seen this exact image in part 1?",color="white", pos=(0,-280)).draw()
		visual.TextStim(win=win,text="Definitely Not",pos=(-230,-320)).draw()
		visual.TextStim(win=win,text="Definitely Yes",pos=(230,-320)).draw()
		drawPlaceholder()
		pics[curTrial['imageFile']]['stim'].draw()
		ratingScale.draw()
		win.flip()
		response= ratingScale.getRating()
		RT = ratingScale.getRT()

	#mark response as correct if response is 1-2 and new or 4-5 and old
	if curTrial['trialType']=='old':
		isRight = int(response==4 or response==5)
	elif curTrial['trialType']=='new':
		isRight = int(response==1 or response==2)
	else:
		isRight = 0

	#write test data to output file
	curTrial['header']=test_header
	trial_data=[curTrial[_] for _ in curTrial['header']] # add independent and runtime variables to what's written to the output file
	#write dependent variables
	trial_data.extend(
		(response,isRight,RT*1000)
		)
	writeToFile(output_file,trial_data,writeNewLine=True)


if __name__ == '__main__':

	#there's a better way than passing all this info out of and into our functions. That better way is called using classes and objects.
	#we'll cover it in class soon
	(study_header, study_trialInfo, test_header, test_trialInfo, study_outputFile, test_outputFile) = initExperiment() #get runtime variables, create trial lists, etc.
	#fullscr=True,
	win = visual.Window([800,800],allowGUI=True, color="gray", units='pix')
	visual.TextStim(win=win,text="Loading stimuli...").draw()
	win.flip()
	pics =  loadFiles('stimuli/visual','.png','image', win=win) #can now access ImageStim objects as pics['filename']['stim']
	fixationCross = visual.TextStim(win=win,text="+",color="black",height=40)


	showInstructions(win)

	# for i,curStudyTrial in enumerate(study_trialInfo):
	# 	showStudyTrial(curStudyTrial,study_header,study_outputFile,pics)

	for i,curTestTrial in enumerate(test_trialInfo):
		showTestTrial(curTestTrial,test_header,test_outputFile,pics)

