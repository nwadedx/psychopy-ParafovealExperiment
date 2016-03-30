#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.83.01), January 17, 2016, at 21:55
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
  
  
"""

# TODO: 

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import locale_setup, visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle, uniform, seed
import os  # handy system and path functions
import sys # to get file system encoding

# OSC imports 
import time, threading
from OSC import *

# Set up OSC receiver.
server = OSCServer( ("localhost", 12345) )
server.addDefaultHandlers()
server.timeout = 0

#global vars
isFixating = 0
timestamp = 0

def eyetech_handler(add, tags, stuff, source):
    global isFixating
    global timestamp
    isFixating = stuff[0]
    timestamp = stuff[1]

server.addMsgHandler("/eyetech", eyetech_handler)
st = threading.Thread(target = server.serve_forever)
st.start()
    

# Set global constants.
foveal_angle = 5.0          # degrees
peripheral_angle = 11.6
distance_from_screen = 177.8   # centimeters (65 in)
cm_per_pixel = (56.5*2.54)/1920.0

# radii given in centimeters.
foveal_radius = 7.76 #abs(distance_from_screen * tan(foveal_angle/2.0))           # 7.76 cm
peripheral_radius = 18.06 #abs(distance_from_screen * tan(peripheral_angle/2.0))   # 18.06 cm

log_dir = 'data\\logs\\'  # log files will be saved with the same filename as the data file 

# Set up point generation functions. TODO: conversion of radius (cm) to pixels (if necessary?).
def foveal():
    r = uniform(0.0, foveal_radius)
    t = uniform(0.0, 360.0)
    
    x = r*cos(t)
    y = r*sin(t)
    
    #x_pix = (1920.0/2)+(x/cm_per_pixel)
    #y_pix = (1080.0/2)-(y/cm_per_pixel)
    
    return [x, y]
    
def peripheral():
    r = uniform(foveal_radius, peripheral_radius)
    t = uniform(0.0, 360.0)
    
    x = r*cos(t)
    y = r*sin(t)
    
    #x_pix = (1920.0/2)+(x/cm_per_pixel)
    #y_pix = (1080.0/2)-(y/cm_per_pixel)
    
    return [x, y]

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'Part 2'  # from the Builder filename that created this script
expInfo = {u'session': u'001', u'participant': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(size=(1920, 1080), fullscr=False, screen=0, allowGUI=True, allowStencil=False,
    monitor='SONY TV', color=[-1.000,-1.000,-1.000], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    )
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# Initialize components for Routine "instructions"
instructionsClock = core.Clock()
instrText = 'At the beginning of every trial, focus your gaze on the fixation mark.\n\nYou will see a series a letters and one or two faces.\n\nWhen you see "Respond now.", press "Z" if the first face was neutral, or press "C" if the first face was angry.\n\nAdditionally, press "B" if the second face was neutral, or press "M" if the second face was angry.\n\nPress SPACEBAR when you are ready to begin.'
text = visual.TextStim(win=win, ori=0, name='text',
    text=instrText, font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "trial"
textSize = 0.15
trialClock = core.Clock()
ISI = core.StaticPeriod(win=win, screenHz=expInfo['frameRate'], name='ISI')
fixation = visual.TextStim(win=win, ori=0, name='fixation',
    text=u'+',    font=u'Arial',
    pos=[0, 0], height=textSize, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=-1.0)
respondText = visual.TextStim(win=win, ori=0, name='response prompt',
    text = 'Respond now.', font=u'Arial',
    pos=[0,0], height=textSize, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=-1.0)
T1 = visual.ImageStim(win=win, name='T1',units='cm', 
    image='sin', mask=None,
    ori=0, pos=[0,0], size=[7, 7],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
T2 = visual.ImageStim(win=win, name='T2', units='cm',
    image=None, mask=None,
    ori=0, pos=[0,0], size=[24, 30],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
d1 = visual.TextStim(win=win, ori=0, name='d1', 
    text='default text',    font=u'Arial',
    pos=[0, 0], height=textSize, wrapWidth=None,
    color=[0.506,0.506,0.506], colorSpace='rgb', opacity=1,
    depth=-5.0)
d2 = visual.TextStim(win=win, ori=0, name='d2', 
    text='default text',    font=u'Arial',
    pos=[0, 0], height=textSize, wrapWidth=None,
    color=[0.506,0.506,0.506], colorSpace='rgb', opacity=1,
    depth=-6.0)
d3 = visual.TextStim(win=win, ori=0, name='d3', 
    text='default text',    font=u'Arial',
    pos=[0, 0], height=textSize, wrapWidth=None,
    color=[0.506,0.506,0.506], colorSpace='rgb', opacity=1,
    depth=-7.0)
d4 = visual.TextStim(win=win, ori=0, name='d4', 
    text='default text',    font=u'Arial',
    pos=[0, 0], height=textSize, wrapWidth=None,
    color=[0.506,0.506,0.506], colorSpace='rgb', opacity=1,
    depth=-8.0)
d5 = visual.TextStim(win=win, ori=0, name='d5', 
    text='default text',    font=u'Arial',
    pos=[0, 0], height=textSize, wrapWidth=None,
    color=[0.506,0.506,0.506], colorSpace='rgb', opacity=1,
    depth=-9.0)
d6 = visual.TextStim(win=win, ori=0, name='d6',
    text='default text',    font=u'Arial',
    pos=[0, 0], height=textSize, wrapWidth=None,
    color=[0.506,0.506,0.506], colorSpace='rgb', opacity=1,
    depth=-10.0)
d7 = visual.TextStim(win=win, ori=0, name='d7', 
    text='default text',    font=u'Arial',
    pos=[0, 0], height=textSize, wrapWidth=None,
    color=[0.506,0.506,0.506], colorSpace='rgb', opacity=1,
    depth=-11.0)
d8 = visual.TextStim(win=win, ori=0, name='d8', 
    text='default text',    font=u'Arial',
    pos=[0, 0], height=textSize, wrapWidth=None,
    color=[0.506,0.506,0.506], colorSpace='rgb', opacity=1,
    depth=-12.0)
d9 = visual.TextStim(win=win, ori=0, name='d9',
    text='default text',    font=u'Arial',
    pos=[0, 0], height=textSize, wrapWidth=None,
    color=[0.506,0.506,0.506], colorSpace='rgb', opacity=1,
    depth=-13.0)
d10 = visual.TextStim(win=win, ori=0, name='d10',
    text='default text',    font=u'Arial',
    pos=[0, 0], height=textSize, wrapWidth=None,
    color=[0.506,0.506,0.506], colorSpace='rgb', opacity=1,
    depth=-14.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

#------Prepare to start Routine "instructions"-------
t = 0
instructionsClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
key_resp_2 = event.BuilderKeyResponse()  # create an object of type KeyResponse
key_resp_2.status = NOT_STARTED
# keep track of which components have finished
instructionsComponents = []
instructionsComponents.append(text)
instructionsComponents.append(key_resp_2)
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "instructions"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = instructionsClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text* updates
    if t >= 0.0 and text.status == NOT_STARTED:
        # keep track of start time/frame for later
        text.tStart = t  # underestimates by a little under one frame
        text.frameNStart = frameN  # exact frame index
        text.setAutoDraw(True)
    
    # *key_resp_2* updates
    if t >= 0.0 and key_resp_2.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_2.tStart = t  # underestimates by a little under one frame
        key_resp_2.frameNStart = frameN  # exact frame index
        key_resp_2.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if key_resp_2.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "instructions"-------
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=30, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('conditions.xlsx'),
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial.keys():
        exec(paramName + '= thisTrial.' + paramName)


# Set up the log file and print headers.
trialLogFile = open(log_dir + '%s_%s_%s' %(expInfo['participant'], expName, expInfo['date']) + '.csv', 'w')
headers = 'trial,T1start,T1image,T1location,lag,T2image,T2location\n'
trialLogFile.write(headers)

nTrial = 1

for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)
    
    #------Prepare to start Routine "trial"-------

    # update component parameters for each repeat
    
    # randomly pick start time (1300, 1400, or 1500 ms), position, and image for T1 based on current conditions
    T1startSec = 1000.0 + (randint(3, 6)*100.0)
    T1start = T1startSec / 1000.0
    print "T1start: %s" % T1start
    T1end = T1start + 0.130
    
    if T1location == 'fovea':
        T1location = foveal()
    else:
        T1location = peripheral()
    
    # randomly select image from dir.
    neutralDir = 'images\\neutral\\'
    angryDir = 'images\\angry\\'
    
    if T1emotion == 'neutral':
        num = randint(1, 6)
        T1image = neutralDir + str(num) + '.jpg'
    else:
        num = randint(1, 6)
        T1image = angryDir + str(num) + '.jpg'
        
    
    T1.pos = (T1location[0], T1location[1])
    T1.setImage(T1image)

    # randomly pick lag
    lags = range(100, 310, 10)    # range = 100-300 ms in steps of 10
    lag = lags[randint(0, len(lags))] / 1000.0

    # randomly pick position and image for T2 based on current conditions
    T2start = T1end + lag
    T2end = T2start + 0.130
    
    if T2location == 'fovea':
        T2location = foveal()
    else:
        T2location = peripheral()
        
    # randomly select image from dir.
    neutralDir = 'images\\neutral\\'
    angryDir = 'images\\angry\\'
    
    if T2emotion == 'neutral':
        num = randint(1, 6)
        T2image = neutralDir + str(num) + '.jpg'
    else:
        num = randint(1, 6)
        T2image = angryDir + str(num) + '.jpg'
    
    T2.pos = (T2location[0], T2location[1])
    T2.setImage(T2image)
    
    # Record all randomly selected data.
    trialData = str(nTrial) + ',' + str(T1start) + ',' + T1image + ',' + (str(T1location[0]) + ' ' + str(T1location[1])) + ',' + str(lag) + ',' + T2image + ',' + (str(T2location[0]) + ' ' + str(T2location[1])) + '\n'
    trialLogFile.write(trialData)
    
    nTrial += 1

    key_resp_3 = event.BuilderKeyResponse()  # create an object of type KeyResponse
    key_resp_3.status = NOT_STARTED


    # randomly pick distractor text.
    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    distractors = [d1, d2, d3, d4, d5, d6, d7, d8, d9, d10]
    d = []

    dNum = 1
    for distractor in distractors:
        # if distractor overlaps with T1 or T2, don't display it.
        overlaps = False
        
        startTime = 1.0 + ((dNum -1)*.130)
        endTime = startTime + 0.130
       
        tRange = range(int(startTime*1000), int(endTime*1000)+130, 130)
        
        
        if (int(T1start*1000) in tRange) or (int(T1end*1000) in tRange) or (int(T2start*1000) in tRange) or (int(T2end*1000) in tRange):
            overlaps = True
        
        if not overlaps:
            seed()
            distractor.setText(letters[randint(0,26)])
            d.append(distractor)  # d will contain only the distractors we want to display
            print distractor.text
            
        dNum += 1
            
    key_resp_3 = event.BuilderKeyResponse()  # create an object of type KeyResponse
    key_resp_3.status = NOT_STARTED
  
  
    # keep track of which components have finished
    trialComponents = []
    trialComponents.append(ISI)
    trialComponents.append(fixation)
    trialComponents.append(respondText)
    trialComponents.append(T1)
    trialComponents.append(T2)
    trialComponents.append(key_resp_3)
    trialComponents.append(d1)
    trialComponents.append(d2)
    trialComponents.append(d3)
    trialComponents.append(d4)
    trialComponents.append(d5)
    trialComponents.append(d6)
    trialComponents.append(d7)
    trialComponents.append(d8)
    trialComponents.append(d9)
    trialComponents.append(d10)
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "trial"-------
    
    # *fixation* updates
    fixation.setAutoDraw(True)
    win.flip()
    
    print "Setting fixation to false."
    
    isFixating = 0         # Since the OSC sender only sends True values         
    while not isFixating:
        if event.getKeys(keyList=["escape"]):
            server.close()
            st.join()
            core.quit()
         
    fixation.setAutoDraw(False)
    win.flip()
    
    t = 1.0
    trialClock.reset(-1.0)  
    frameN = -1
    routineTimer.add(20.0)
    
    continueRoutine = True
    printThing = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fixation* updates
        '''
        if t >= 0.0 and fixation.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixation.tStart = t  # underestimates by a little under one frame
            fixation.frameNStart = frameN  # exact frame index
            fixation.setAutoDraw(True)
        if fixation.status == STARTED and t >= (0.0 + (1-win.monitorFramePeriod*0.75)): #most of one frame period left
            fixation.setAutoDraw(False)
            '''
            
        # *T1* updates
        if t >= T1start and T1.status == NOT_STARTED:
            # keep track of start time/frame for later
            T1.tStart = t  # underestimates by a little under one frame
            T1.frameNStart = frameN  # exact frame index
            T1.setAutoDraw(True)
            print "T1 starting: %s" % t
        if T1.status == STARTED and t >= (T1start + (.130-win.monitorFramePeriod*0.75)): #most of one frame period left
            T1.setAutoDraw(False)
        
        # *T2* updates
        if t >= T2start and T2.status == NOT_STARTED:
            # keep track of start time/frame for later
            T2.tStart = t  # underestimates by a little under one frame
            T2.frameNStart = frameN  # exact frame index
            T2.setAutoDraw(True)
            print "T2 starting: %s" % t
        if T2.status == STARTED and t >= (T2start + (.130-win.monitorFramePeriod*0.75)): #most of one frame period left
            T2.setAutoDraw(False)
      
        # *key_resp_3* updates
        if t >= 2.300 and key_resp_3.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_resp_3.tStart = t  # underestimates by a little under one frame
            key_resp_3.frameNStart = frameN  # exact frame index
            key_resp_3.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if key_resp_3.status == STARTED and t >= (2.300 +(5-win.monitorFramePeriod*0.75)): #most of one frame period left
            key_resp_3.status = STOPPED
        if key_resp_3.status == STARTED:
            theseKeys = event.getKeys(keyList=['z', 'c', 'b', 'm'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                for key in theseKeys:
                    key_resp_3.keys.append(key)
                    key_resp_3.rt.append(key_resp_3.clock.getTime())
                key_resp_3.corr = 0   # just record everything as incorrect and throw it out later in post; don't want to risk changing correct answer collection in case it'll break
        
        # *d1* updates
        if t >= 1.0 and d1.status == NOT_STARTED and (d1 in d):
            # keep track of start time/frame for later
            d1.tStart = t  # underestimates by a little under one frame
            d1.frameNStart = frameN  # exact frame index
            d1.setAutoDraw(True)
            print "d1 starting: %s" % t
        if d1.status == STARTED and t >= (1 + (.130-win.monitorFramePeriod*0.75)): #most of one frame period left
            d1.setAutoDraw(False)
        
        # *d2* updates
        if t >= 1.130 and d2.status == NOT_STARTED and (d2 in d):
            # keep track of start time/frame for later
            d2.tStart = t  # underestimates by a little under one frame
            d2.frameNStart = frameN  # exact frame index
            d2.setAutoDraw(True)
            print "d2 starting: %s" % t
        if d2.status == STARTED and t >= (1.130 + (.130-win.monitorFramePeriod*0.75)): #most of one frame period left
            d2.setAutoDraw(False)
        
        # *d3* updates
        if t >= 1.260 and d3.status == NOT_STARTED and (d3 in d):
            # keep track of start time/frame for later
            d3.tStart = t  # underestimates by a little under one frame
            d3.frameNStart = frameN  # exact frame index
            d3.setAutoDraw(True)
        if d3.status == STARTED and t >= (1.260 + (.130-win.monitorFramePeriod*0.75)): #most of one frame period left
            d3.setAutoDraw(False)
        
        # *d4* updates
        if t >= 1.390 and d4.status == NOT_STARTED and (d4 in d):
            # keep track of start time/frame for later
            d4.tStart = t  # underestimates by a little under one frame
            d4.frameNStart = frameN  # exact frame index
            d4.setAutoDraw(True)
        if d4.status == STARTED and t >= (1.390 + (0.130-win.monitorFramePeriod*0.75)): #most of one frame period left
            d4.setAutoDraw(False)
        
        # *d5* updates
        if t >= 1.520 and d5.status == NOT_STARTED and (d5 in d):
            # keep track of start time/frame for later
            d5.tStart = t  # underestimates by a little under one frame
            d5.frameNStart = frameN  # exact frame index
            d5.setAutoDraw(True)
        if d5.status == STARTED and t >= (1.520 + (0.130-win.monitorFramePeriod*0.75)): #most of one frame period left
            d5.setAutoDraw(False)
        
        # *d6* updates
        if t >= 1.650 and d6.status == NOT_STARTED and (d6 in d):
            # keep track of start time/frame for later
            d6.tStart = t  # underestimates by a little under one frame
            d6.frameNStart = frameN  # exact frame index
            d6.setAutoDraw(True)
        if d6.status == STARTED and t >= (1.650 + (0.130-win.monitorFramePeriod*0.75)): #most of one frame period left
            d6.setAutoDraw(False)
        
        # *d7* updates
        if t >= 1.780 and d7.status == NOT_STARTED and (d7 in d):
            # keep track of start time/frame for later
            d7.tStart = t  # underestimates by a little under one frame
            d7.frameNStart = frameN  # exact frame index
            d7.setAutoDraw(True)
        if d7.status == STARTED and t >= (1.780 + (0.130-win.monitorFramePeriod*0.75)): #most of one frame period left
            d7.setAutoDraw(False)
        
        # *d8* updates
        if t >= 1.910 and d8.status == NOT_STARTED and (d8 in d):
            # keep track of start time/frame for later
            d8.tStart = t  # underestimates by a little under one frame
            d8.frameNStart = frameN  # exact frame index
            d8.setAutoDraw(True)
        if d8.status == STARTED and t >= (1.910 + (0.130-win.monitorFramePeriod*0.75)): #most of one frame period left
            d8.setAutoDraw(False)
        
        # *d9* updates
        if t >= 2.040 and d9.status == NOT_STARTED and (d9 in d):
            # keep track of start time/frame for later
            d9.tStart = t  # underestimates by a little under one frame
            d9.frameNStart = frameN  # exact frame index
            d9.setAutoDraw(True)
        if d9.status == STARTED and t >= (2.040 + (0.130-win.monitorFramePeriod*0.75)): #most of one frame period left
            d9.setAutoDraw(False)
        
        # *d10* updates
        if t >= 2.170 and d10.status == NOT_STARTED and (d10 in d):
            # keep track of start time/frame for later
            d10.tStart = t  # underestimates by a little under one frame
            d10.frameNStart = frameN  # exact frame index
            d10.setAutoDraw(True)
        if d10.status == STARTED and t >= (2.170 + (0.130-win.monitorFramePeriod*0.75)): #most of one frame period left
            d10.setAutoDraw(False)
            
        # *respondText* updates
        if t >= 2.300 and respondText.status == NOT_STARTED:
            # keep track of start time/frame for later
            respondText.tStart = t  # underestimates by a little under one frame
            respondText.frameNStart = frameN  # exact frame index
            respondText.setAutoDraw(True)
        if respondText.status == STARTED and t >= (2.300 + (5-win.monitorFramePeriod*0.75)): #most of one frame period left
            respondText.setAutoDraw(False)
            
        if t >= 7.300:
            continueRoutine = False
            
        '''
        # *ISI* period
        if t >= 0.0 and ISI.status == NOT_STARTED:
            # keep track of start time/frame for later
            ISI.tStart = t  # underestimates by a little under one frame
            ISI.frameNStart = frameN  # exact frame index
            ISI.start(0.5)
        elif ISI.status == STARTED: #one frame should pass before updating params and completing
            ISI.complete() #finish the static period
            '''
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
                
               
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            server.close()
            st.join()
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_3.keys in ['', [], None]:  # No response was made
       key_resp_3.keys=None
       # was no response the correct answer?!
       key_resp_3.corr = 0  # failed to respond (incorrectly)
    # store data for  (TrialHandler)
    trials.addData('key_resp_3.keys',key_resp_3.keys)
    trials.addData('key_resp_3.corr', key_resp_3.corr)
    if key_resp_3.keys != None:  # we had a response
        trials.addData('key_resp_3.rt', key_resp_3.rt)
    thisExp.nextEntry()
    
# completed 30 repeats of 'trials'
server.close()
st.join()
trialLogFile.close()
win.close()
core.quit()
