#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.82.01), Thu Nov 19 21:04:07 2015
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import locale_setup, visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import os  # handy system and path functions
from psychopy.hardware.emulator import launchScan
import socket
from time import time, sleep
import json

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))  # .decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

triggerId = 0


def choose_session():
    dlg = gui.Dlg(title='Session Number')
    dlg.addField('number:', choices=["One", "Two", "Three", 'Four', 'Five', 'Six'])
    number = dlg.show()
    return number[0]


def config_experiment():
    # Store info about the experiment session
    exp_name = 'DecoderConst_fMRI'  # from the Builder filename that created this script
    exp_info = {u'session': u'001', u'participant': u''}
    dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)
    if not dlg.OK:
        core.quit()  # user pressed cancel
    exp_info['date'] = data.getDateStr()  # add a simple timestamp
    exp_info['exp_name'] = exp_name

    return exp_name, exp_info, 0


def make_file_name(exp_name, exp_info):
    # Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    file_name = _thisDir + os.sep + 'data/%s_%s_%s' % (exp_info['participant'], exp_name, exp_info['date'])
    return file_name


def define_exp_handler(exp_name, exp_info, file_name):
    # An ExperimentHandler isn't essential but helps with data saving
    this_exp = data.ExperimentHandler(name=exp_name, version='',
                                      extraInfo=exp_info, runtimeInfo=None,
                                      originPath=None,
                                      savePickle=True, saveWideText=True,
                                      dataFileName=file_name)
    return this_exp


def set_log_file(file_name):
    # save a log file for detail verbose info
    _log_file = logging.LogFile(file_name + '.log', level=logging.EXP)
    return _log_file


def set_launch_scan():
    # settings for launchScan:
    mr_settings = {
        'TR': 2.000,  # duration (sec) per whole-brain volume
        'volumes': 5,  # number of whole-brain 3D volumes per scanning run
        'sync': 't',  # character to use as the sync timing event; assumed to come at start of a volume
        'skip': 0,  # number of volumes lacking a sync pulse at start of scan (for T1 stabilization)
        'sound': True  # in test mode: play a tone as a reminder of scanner noise
    }
    return mr_settings


def show_launch_dialog(mr_settings):
    info_dlg = gui.DlgFromDict(mr_settings, title='fMRI parameters', order=['TR', 'volumes'])
    return info_dlg


def set_window():
    # Set up the Window
    _win = visual.Window(size=(1440, 900), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
                         monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb',
                         blendMode='avg', useFBO=True, )
    return _win


def get_frame_rate_duration():
    # store frame rate of monitor if we can measure it successfully
    frame_rate = win.getActualFrameRate()
    if frame_rate is not None:
        frame_dur = 1.0 / frame_rate
    else:
        frame_dur = 1.0 / 60.0  # couldn't get a reliable measure so guess
    return frame_rate, frame_dur


def init_instructions():
    # Initialize components for Routine "Instruction"
    clock = core.Clock()
    image = visual.ImageStim(win=win, name='image',
                             image=None, mask=None,
                             ori=0, pos=[0, 0], size=[10, 10],
                             color=[1, 1, 1], colorSpace='rgb', opacity=1,
                             flipHoriz=False, flipVert=False,
                             texRes=128, interpolate=True, depth=0.0)
    return clock, image


def init_trial():
    clock = core.Clock()
    isi = core.StaticPeriod(win=win, screenHz=expInfo['frameRate'], name='ISI')
    image = visual.ImageStim(win=win, name='image_2',
                             image=None, mask=None,
                             ori=0, pos=[0, 0], size=[10, 10],
                             color=[1, 1, 1], colorSpace='rgb', opacity=1,
                             flipHoriz=False, flipVert=False,
                             texRes=128, interpolate=True, depth=-1.0)
    image_pres = visual.ImageStim(win=win, name='imagePres',
                                  image='sin', mask=None,
                                  ori=0, pos=[0, 0], size=1,
                                  color=[1.000, 1.000, 1.000], colorSpace='rgb', opacity=1,
                                  flipHoriz=False, flipVert=False,
                                  texRes=128, interpolate=True, depth=-2.0)
    return clock, isi, image, image_pres


def init_end():
    end_clock = core.Clock()
    text = visual.TextStim(win=win, ori=0, name='text_2',
                           text='Thanks!', font='Arial',
                           pos=[0, 0], height=0.1, wrapWidth=None,
                           color='Black', colorSpace='rgb', opacity=1,
                           depth=0.0)
    img = visual.ImageStim(win=win, name='image_3',
                           image=None, mask=None,
                           ori=0, pos=[0, 0], size=[10, 10],
                           color=[1, 1, 1], colorSpace='rgb', opacity=1,
                           flipHoriz=False, flipVert=False,
                           texRes=128, interpolate=True, depth=-2.0)
    return end_clock, text, img


def log_run_timing(mr_settings):
    # summary of run timing, for each key press:
    _output = 'vol    onset key\n'
    for i in range(-1 * mr_settings['skip'], 0):
        _output += u'%d prescan skip (no sync)\n' % i

    _counter = visual.TextStim(win, height=.05, pos=(0, 0), color=win.rgb + 0.5)
    _output += u"  0    0.000 sync  [Start of scanning run, vol 0]\n"
    return _output, _counter


def set_test_or_scan(_win, mr_settings, global_clock, _counter):
    # launch: operator selects Scan or Test (emulate); see API documentation
    _vol = launchScan(_win, mr_settings, globalClock=global_clock)
    _counter.setText(u"%d volumes\n%.3f seconds" % (0, 0.0))
    _counter.draw()
    win.flip()
    return _vol, _counter


def send_trigger(eve, value):
    print('TRIGGER', eve, value)

    global trig_id

    trig_id += 1

    timestamp = time()
    data_to_send = {
        "id": trig_id,
        "timestamp": int(timestamp * 1e9),
        "event": eve,
        "value": value,
    }
    event = json.dumps(data_to_send).encode("utf-8")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(event, ("239.128.35.86", 7891))


session_number = choose_session()
excel_file = "./run" + session_number + ".xlsx"

expName, expInfo, trig_id = config_experiment()
fileName = make_file_name(expName, expInfo)

thisExp = define_exp_handler(expName, expInfo, fileName)

log_file = set_log_file(fileName)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

MR_settings = set_launch_scan()
infoDlg = show_launch_dialog(MR_settings)
if not infoDlg.OK:
    core.quit()

# Start Code - component code to be run before the window creation

win = set_window()

frameRate, frameDur = get_frame_rate_duration()
expInfo['frameRate'] = frameRate

InstructionClock, image = init_instructions()

trialClock, ISI, image_2, imagePres = init_trial()

EndClock, text_2, image_3 = init_end()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

output, counter = log_run_timing(MR_settings)

# launch: operator selects Scan or Test (emulate); see API documentation

vol, counter = set_test_or_scan(win, MR_settings, globalClock, counter)

duration = MR_settings['volumes'] * MR_settings['TR']

# note: globalClock has been reset to 0.0 by launchScan() in set_test_or_scan
while globalClock.getTime() < duration:
    allKeys = event.getKeys()
    for key in allKeys:
        if key == MR_settings['sync']:
            onset = globalClock.getTime()
            # do your experiment code at this point if you want it sync'd to the TR
            # for demo just display a counter & time, updated at the start of each TR

            # ------Prepare to start Routine "Instruction"-------
            t = 0
            InstructionClock.reset()  # clock 
            routineTimer.reset()
            routineTimer.add(20.000000)
            frameN = -1
            # update component parameters for each repeat
            key_resp_3 = event.BuilderKeyResponse()  # create an object of type KeyResponse
            key_resp_3.status = NOT_STARTED
            # keep track of which components have finished
            InstructionComponents = [image, key_resp_3]
            for thisComponent in InstructionComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # -------Start Routine "Instruction"-------
            continueRoutine = False
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = InstructionClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # *image* updates
                if t >= 0.0 and image.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    image.tStart = t  # underestimates by a little under one frame
                    image.frameNStart = frameN  # exact frame index
                    image.setAutoDraw(True)
                if image.status == STARTED and t >= (
                        0.0 + (20.0 - win.monitorFramePeriod * 0.75)):  # most of one frame period left
                    image.setAutoDraw(False)

                # *key_resp_3* updates
                if t >= 0.0 and key_resp_3.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    key_resp_3.tStart = t  # underestimates by a little under one frame
                    key_resp_3.frameNStart = frameN  # exact frame index
                    key_resp_3.status = STARTED
                    # keyboard checking is just starting
                    win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
                    event.clearEvents(eventType='keyboard')
                if key_resp_3.status == STARTED and t >= (
                        0.0 + (20 - win.monitorFramePeriod * 0.75)):  # most of one frame period left
                    key_resp_3.status = STOPPED
                if key_resp_3.status == STARTED:
                    theseKeys = event.getKeys()

                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0:  # at least one key was pressed
                        key_resp_3.keys.extend(theseKeys)  # storing all keys
                        key_resp_3.rt.append(key_resp_3.clock.getTime())

                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component is still running
                for thisComponent in InstructionComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over, or we'll get a blank screen
                    win.flip()

            # -------Ending Routine "Instruction"-------
            for thisComponent in InstructionComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # check responses
            if key_resp_3.keys in ['', [], None]:  # No response was made
                key_resp_3.keys = None
            # store data for thisExp (ExperimentHandler)
            thisExp.addData('key_resp_3.keys', key_resp_3.keys)
            if key_resp_3.keys is not None:  # we had a response
                thisExp.addData('key_resp_3.rt', key_resp_3.rt)
            thisExp.nextEntry()

            # set up handler to look after randomisation of conditions etc
            trials = data.TrialHandler(nReps=1, method='sequential',
                                       extraInfo=expInfo, originPath=-1,
                                       trialList=data.importConditions(excel_file),
                                       seed=None, name='trials')
            thisExp.addLoop(trials)  # add the loop to the experiment
            thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
            if thisTrial is not None:
                for paramName in thisTrial.keys():
                    exec(paramName + '= thisTrial.' + paramName)
            send_trigger('start_experiment', '1')
            for trial_index, thisTrial in enumerate(trials):
                currentLoop = trials
                # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
                if thisTrial.Stimuli is not None:
                    stimuli = thisTrial.Stimuli
                    for paramName in thisTrial.keys():
                        exec(paramName + '= thisTrial.' + paramName)

                    # ------Prepare to start Routine "trial"-------
                    t = 0
                    trialClock.reset()  # clock
                    routineTimer.reset()

                    frameN = -1
                    routineTimer.add(0.960000)
                    # update component parameters for each repeat
                    imagePres.setPos([0, 0])
                    imagePres.setImage('../img/' + Stimuli)
                    key_resp_4 = event.BuilderKeyResponse()  # create an object of type KeyResponse
                    key_resp_4.status = NOT_STARTED
                    # keep track of which components have finished
                    trialComponents = [ISI, image_2, imagePres, key_resp_4]
                    for thisComponent in trialComponents:
                        if hasattr(thisComponent, 'status'):
                            thisComponent.status = NOT_STARTED

                    # -------Start Routine "trial"-------

                    print(trialClock.getTime())
                    # send_trigger('start_experiment', '1')
                    continueRoutine = True
                    cntr = 0
                    while continueRoutine and routineTimer.getTime() > 0:
                        cntr += 1
                        # print(cntr)
                        # get current time
                        t = trialClock.getTime()
                        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                        # update/draw components on each frame

                        # *image_2* updates
                        if t >= 0.0 and image_2.status == NOT_STARTED:
                            # keep track of start time/frame for later
                            image_2.tStart = t  # underestimates by a little under one frame
                            image_2.frameNStart = frameN  # exact frame index
                            image_2.setAutoDraw(True)
                        if image_2.status == STARTED and t >= (
                                0.0 + (0.96 - win.monitorFramePeriod * 0.75)):  # most of one frame period left
                            image_2.setAutoDraw(False)

                        # *imagePres* updates
                        if t >= 0 and imagePres.status == NOT_STARTED:
                            # keep track of start time/frame for later
                            imagePres.tStart = t  # underestimates by a little under one frame
                            imagePres.frameNStart = frameN  # exact frame index
                            imagePres.setAutoDraw(True)
                        if imagePres.status == STARTED and t >= (
                                0 + (0.96 - win.monitorFramePeriod * 0.75)):  # most of one frame period left
                            imagePres.setAutoDraw(False)

                        # *key_resp_4* updates
                        if t >= 0.0 and key_resp_4.status == NOT_STARTED:
                            # keep track of start time/frame for later
                            key_resp_4.tStart = t  # underestimates by a little under one frame
                            key_resp_4.frameNStart = frameN  # exact frame index
                            key_resp_4.status = STARTED
                            # keyboard checking is just starting
                            win.callOnFlip(key_resp_4.clock.reset)  # t=0 on next screen flip
                        if key_resp_4.status == STARTED and t >= (
                                0.0 + (0.96 - win.monitorFramePeriod * 0.75)):  # most of one frame period left
                            key_resp_4.status = STOPPED
                        if key_resp_4.status == STARTED:
                            theseKeys = event.getKeys()

                            # check for quit:
                            if "escape" in theseKeys:
                                endExpNow = True
                            if len(theseKeys) > 0:  # at least one key was pressed
                                key_resp_4.keys.extend(theseKeys)  # storing all keys
                                key_resp_4.rt.append(key_resp_4.clock.getTime())
                                # was this 'correct'?
                                if (key_resp_4.keys == str(u'correctAns')) or (key_resp_4.keys == u'correctAns'):
                                    key_resp_4.corr = 1
                                else:
                                    key_resp_4.corr = 0
                        # *ISI* period
                        if t >= 0 and ISI.status == NOT_STARTED:
                            # keep track of start time/frame for later
                            ISI.tStart = t  # underestimates by a little under one frame
                            ISI.frameNStart = frameN  # exact frame index
                            ISI.start(0.96 - t)
                        elif ISI.status == STARTED:  # one frame should pass before updating params and completing
                            ISI.complete()  # finish the static period

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
                            core.quit()

                        # refresh the screen
                        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                            win.flip()
                            if cntr == 1:
                                send_trigger('event_stim', Condition + '-' + stimuli.replace('_', '-'))

                                # if trial_index > 0:
                                #     send_trigger('end_trial', '0')
                                # send_trigger('start_trial', Condition + '-' + stimuli.replace('_', '-'))


                    # -------Ending Routine "trial"-------
                    for thisComponent in trialComponents:
                        if hasattr(thisComponent, "setAutoDraw"):
                            thisComponent.setAutoDraw(False)
                    # check responses
                    if key_resp_4.keys in ['', [], None]:  # No response was made
                        key_resp_4.keys = None
                        # was no response the correct answer?!
                        if str(u'correctAns').lower() == 'none':
                            key_resp_4.corr = 1  # correct non-response
                        else:
                            key_resp_4.corr = 0  # failed to respond (incorrectly)
                    # store data for trials (TrialHandler)
                    trials.addData('key_resp_4.keys', key_resp_4.keys)
                    trials.addData('key_resp_4.corr', key_resp_4.corr)
                    if key_resp_4.keys != None:  # we had a response
                        trials.addData('key_resp_4.rt', key_resp_4.rt)
                    # send_trigger('end_experiment', '0')
                    thisExp.nextEntry()

            # completed 1 repeats of 'trials'

            # ------Prepare to start Routine "End"-------
            t = 0
            EndClock.reset()  # clock 
            routineTimer.reset()
            send_trigger('end_experiment', '0')
            frameN = -1
            routineTimer.add(9.000000)
            # update component parameters for each repeat
            key_resp_2 = event.BuilderKeyResponse()  # create an object of type KeyResponse
            key_resp_2.status = NOT_STARTED
            # keep track of which components have finished
            EndComponents = []
            EndComponents.append(text_2)
            EndComponents.append(key_resp_2)
            EndComponents.append(image_3)
            for thisComponent in EndComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # -------Start Routine "End"-------
            continueRoutine = True
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = EndClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # *text_2* updates
                if t >= 0.0 and text_2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    text_2.tStart = t  # underestimates by a little under one frame
                    text_2.frameNStart = frameN  # exact frame index
                    text_2.setAutoDraw(True)
                if text_2.status == STARTED and t >= (
                        0.0 + (9 - win.monitorFramePeriod * 0.75)):  # most of one frame period left
                    text_2.setAutoDraw(False)

                # *key_resp_2* updates
                if t >= 0.0 and key_resp_2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    key_resp_2.tStart = t  # underestimates by a little under one frame
                    key_resp_2.frameNStart = frameN  # exact frame index
                    key_resp_2.status = STARTED
                    # keyboard checking is just starting
                    win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
                    event.clearEvents(eventType='keyboard')
                if key_resp_2.status == STARTED and t >= (
                        0.0 + (9 - win.monitorFramePeriod * 0.75)):  # most of one frame period left
                    key_resp_2.status = STOPPED
                if key_resp_2.status == STARTED:
                    theseKeys = event.getKeys()

                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0:  # at least one key was pressed
                        key_resp_2.keys = theseKeys[-1]  # just the last key pressed
                        key_resp_2.rt = key_resp_2.clock.getTime()
                        # a response ends the routine
                        # continueRoutine = False

                # *image_3* updates
                if t >= 0.0 and image_3.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    image_3.tStart = t  # underestimates by a little under one frame
                    image_3.frameNStart = frameN  # exact frame index
                    image_3.setAutoDraw(True)
                if image_3.status == STARTED and t >= (
                        0.0 + (9.0 - win.monitorFramePeriod * 0.75)):  # most of one frame period left
                    image_3.setAutoDraw(False)

                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in EndComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()

            # -------Ending Routine "End"-------
            for thisComponent in EndComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # check responses
            if key_resp_2.keys in ['', [], None]:  # No response was made
                key_resp_2.keys = None
            # store data for thisExp (ExperimentHandler)
            thisExp.addData('key_resp_2.keys', key_resp_2.keys)
            if key_resp_2.keys != None:  # we had a response
                thisExp.addData('key_resp_2.rt', key_resp_2.rt)
        else:
            # handle keys (many fiber-optic buttons become key-board key-presses)
            output += u"%3d  %7.3f %s\n" % (vol - 1, globalClock.getTime(), unicode(key))
            if key == 'escape':
                break

thisExp.nextEntry()
# the Routine "End" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()
win.close()
core.quit()
