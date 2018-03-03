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

	return (header, trialInfo, outputFile)


def makePlaceholder(lineColor="black", fillColor="white",pos=(0,0)):
	"""
	creates a white placeholder for an image. Makes things look nice.
	"""
	return visual.Rect(win=win,size=(650,450), lineColor=lineColor, fillColor=fillColor, lineWidth=2)


def showIntroDisplay(curTrial,pics):
	"""
	this function should show the images for the first trial of the block. 
	if subject is in the labeled (wDescr) condition, show the image labels below each image
	Show the images for 30 seconds; then blank the screen, and show "Ready?" before starting the learning trials 
	No need to write any data for the intro trials.

	use calculateRectangularCoordinates() (see useful_functions.py) to dynamically create a positions dictionary and use 
	it to position placeholders and draw the Droodle images on top of the placeholders, i.e., draw placeholders, then draw your images
	The positions should change depending on how many images you're showing on a given block, e.g., 4 might be arranged 2x2, 6, 3x2
	You can then refer to the positions something like this: positions[curTrial['numImages'][0]] would return the position of the first image
	on a block that has numImages number of images. (curTrial['numImages'] would evaluate to a number.. 
	"""
	pass


def showLearningTrial(curTrial,header,output_file,pics,sounds):
	win.flip()
	core.wait(preFixationDelay) 
	makePlaceholder().draw()
	fixationCross.draw()
	win.flip()
	core.wait(postFixationDelay)


	#insert code related to showing a learning trial. These are identical for people in wDescr and noDescr conditions 

	isRight=1 #set this as needed
	RT = 0 #set this as needed
	
	#write data to output file
	curTrial['header']=header
	trial_data=[curTrial[_] for _ in curTrial['header']] # add independent and runtime variables to what's written to the output file
	#write dependent variables
	trial_data.extend(
		(isRight,RT)
		)
	writeToFile(output_file,trial_data,writeNewLine=True)



if __name__ == '__main__':

	(header, trialInfo, outputFile) = initExperiment() #get runtime variables, create trial lists, etc.
	#there's a better way than passing all this info out of and into our functions. That better way is called using classes and objects.
	#we'll cover it in class soon

	win = visual.Window(fullscr=True,allowGUI=False, color="gray", units='pix')
	pics =  loadFiles('stimuli/visual','.png','image', win=win) #can now access ImageStim objects as pics['filename']['stim']
	sounds =  loadFiles('stimuli/sounds','.wav','sound', win=win) #can now access ImageStim objects as pics['filename']['stim']

	fixationCross = visual.TextStim(win=win,text="+",color="black",height=40)


	#show instructions etc.

	for i,curTrial in enumerate(trialInfo):
		showIntro=False #will need to figure out when to set this to True
		if showIntro:
			showIntroDisplay(curTrial,pics)
		else:
			#will need to figure out how to stop showing these and go to the next block is subject's performance meets the specs
			showLearningTrial(curTrial,header,outputFile,pics,sounds)






