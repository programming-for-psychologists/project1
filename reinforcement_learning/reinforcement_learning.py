from psychopy import core, visual, prefs, event
import random
import sys
import copy
from useful_functions import *
from generateTrials import *


expName='reinforcement_learning_v1'
preFixationDelay = .75
postFixationDelay = .5
stimDuration = 1.0

postSoundDelayCorrect = 0.1
postSoundDelayIncorrect = 1.0
runningAverageWindow = 10
minAccuracy = 0.6
validResponses = ['z','x','c']


def initExperiment():

	while True:
		runTimeVarOrder = ['subjCode','seed','gender','condition']
		runTimeVars = getRunTimeVars({'subjCode':'reinf_learn_101', 'seed':10, 'gender':['Choose', 'male','female','other'], 'condition': ['Choose', 'wDescr', 'noDescr']},runTimeVarOrder,expName)
		if runTimeVars['subjCode']=='':
			popupError('Subject code is blank')				
		elif 'Choose' in runTimeVars.values():
			popupError('Need to choose a value from a dropdown box')
		else:
			try:
				outputFile = openOutputFile('data/'+runTimeVars['subjCode'],expName+'_learning.csv')
				if outputFile: #file(s) were able to be opened
					break
			except:
				popupError('Output file(s) could not be opened')

	generateTrials(runTimeVars,runTimeVarOrder)

	(header,trialInfo) = importTrialsWithHeader('trials/'+runTimeVars['subjCode']+'_trials.csv')
	trialInfo = evaluateLists(trialInfo)

	return (header, trialInfo, outputFile)


def makePlaceholder(lineColor="gray", fillColor="white",pos=(0,0)):
	"""
	creates a white placeholder for an image. Makes things look nice.
	"""
	return visual.Rect(win=win,size=(700,500), lineColor=lineColor, fillColor=fillColor, lineWidth=1)

def showAttentionDisplay():
	visual.TextStim(win=win,text="Please try to respond more accurately. Press any key to proceed.",color="darkred",height=40).draw()
	win.flip()
	event.waitKeys()


def showInstructions():
	visual.TextStim(win=win,text="Instructions go here.",color="darkred",height=40).draw()
	win.flip()
	event.waitKeys()


def showIntroDisplay(curTrial,stim_names_descriptions):


	if curTrial['numStimsInBlock']=='3':
		positions = calculateRectangularCoordinates(300,0,3,1)
		instructionPos = (0,200)
	elif curTrial['numStimsInBlock']=='4':
		positions = calculateRectangularCoordinates(300,260,2,2)
		instructionPos = (0,300)
	elif curTrial['numStimsInBlock']=='6':
		positions = calculateRectangularCoordinates(300,260,3,2)
		instructionPos = (0,300)


	instructionText = "In this block, you will be learning to associate the shapes below with the keys 'z', 'x', and 'c'.\n \
	Begin by guessing. You will received feedback based on your response. If you responded correctly (bleep sound) or incorrectly (buzz sound)\n \
	Note that several images may map onto the same key. For example, the first and second image may both map onto the 'x' key."

	visual.TextStim(win=win,text=instructionText,color="black",height=20, pos=instructionPos).draw()


	for itemNum, (curPic,curDescription) in enumerate(stim_names_descriptions.items()):
		pics[curPic]['stim'].setPos(positions[itemNum])
		pics[curPic]['stim'].draw()
		if curTrial['condition']=='wDescr':
			visual.TextStim(win=win,text=curDescription,color="black",height=22, pos=(positions[itemNum][0], positions[itemNum][1]-115)).draw()
	win.flip()
	event.waitKeys()



def showLearningTrial(curTrial,header,output_file,pics,sounds):
	win.flip()
	core.wait(preFixationDelay) 
	makePlaceholder().draw()
	pics[curTrial['stim']]['stim'].setPos((0,0))
	pics[curTrial['stim']]['stim'].draw()
	win.flip()
	(response, RT) = getKeyboardResponse(validResponses)
	if response == curTrial['key']:
		isRight=1
		sounds['bleep']['stim'].play()
	else:
		isRight=0
		sounds['buzz']['stim'].play()
	
	#write data to output file
	curTrial['header']=header
	trial_data=[curTrial[_] for _ in curTrial['header']] # add independent and runtime variables to what's written to the output file
	#write dependent variables
	trial_data.extend(
		(response,isRight,RT)
		)
	writeToFile(output_file,trial_data,writeNewLine=True)
	return isRight


if __name__ == '__main__':

	(header, trialInfo, outputFile) = initExperiment() #get runtime variables, create trial lists, etc.
	#there's a better way than passing all this info out of and into our functions. That better way is using classes and objects.
	#we'll cover it in class soon

	win = visual.Window([1000,780],allowGUI=True, color="white", units='pix')
	pics =  loadFiles('stimuli/visual','.png','image', win=win) #can now access ImageStim objects as pics['filename']['stim']
	sounds =  loadFiles('stimuli/sounds','.wav','sound', win=win) #can now access ImageStim objects as pics['filename']['stim']

	fixationCross = visual.TextStim(win=win,text="+",color="black",height=20)

	showInstructions()
	shownAt=0
	for trialIndex,curTrial in enumerate(trialInfo):
		showIntro=False #will need to figure out when to set this to True
		if curTrial['trialIndex'] == '0': 		#we're on the 0th trial, so show an intro screen.
			#but... we need to know what the stimulus names and descriptions are, so let's iterate through the current block and collect them
			stim_names_descriptions={stimInfo['stim']:stimInfo['description'] for stimInfo in trialInfo if stimInfo['block']==curTrial['block']}
			print "name to value mapping", stim_names_descriptions
			showIntroDisplay(curTrial,stim_names_descriptions)
			accuracies = []

		#show learning trial; this is executed regardless of whether we're on trial 0 or after
		isRight = showLearningTrial(curTrial,header,outputFile,pics,sounds)
		accuracies.append(isRight)

		#if we've past trial 10 and the accuracies for the last runningAverageWindow trials are below minAccuracy
		#AND we haven't shown the attention display in the last 10 trials, then show it.
		if trialIndex>=10 and np.mean(accuracies[-(runningAverageWindow-1):])<minAccuracy and trialIndex > shownAt+10:
			showAttentionDisplay()
			shownAt = trialIndex

