import os
import re
import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
import time
import sys
import platform
import subprocess
import shutil

#Import the common code - basically the SqueezePlayer class
#which connects to the server and a player
from b808common import *
from XSqueezeCommon import *

#an orderly place to keep XSqueeze specific constants
import constants

#the window for the README
from ReadMeViewer import *

#the window class
from NowPlayingWindow import *

################################################################################
# Do some cleanup (even if we are exiting early)

def cleanup(andexit=True):

    global xbmcAudioSuspended, slaveProcess

    logNotice("Doing Cleanup")

    #are we running the locally installed Squeezeslave? KILL IT!
    if constants.PLAYBACK and slaveProcess is not None:
        logNotice("Killing player process...")
        try:
            slaveProcess.terminate()
        except Exception as inst:
            logNotice("Error killing player, probably the player crashed.  Let's try re-start it so we can grab the output for debugging!")
            #now let's try to start it again so we can log the output message for clues...
            if constants.SYSTEM.startswith("win"):
                output, result = subprocess.Popen(exe, creationflags=0x08000000, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=False).communicate()
            else:
                output, result = subprocess.Popen(exe, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=False).communicate()
            logNotice("ERROR RESULT: " + str(result))
            logNotice("ERROR OUTPUT: " + str(output))

    #Try and resume XBMC's AudioEngine if we suspended it
    if xbmcAudioSuspended:
        try:
            #pause
            if constants.SECONDS_TO_PAUSE_EXIT!=0:
                logNotice("Pausing for " + str(constants.SECONDS_TO_PAUSE_EXIT) + ", per request in XSqueeze settings.")
                notify("Pause & resume AE after " + str(constants.SECONDS_TO_PAUSE_EXIT) + " seconds.", "(per request in XSqueeze settings.)")
                time.sleep(constants.SECONDS_TO_PAUSE_EXIT)
            xbmc.audioResume();
            logNotice("Resumed XBMC AE")
        except:
            pass

    #remove our custom keymap
    try:
        os.remove(constants.KEYMAPDESTFILE)
        logNotice("Removed custom keymap")
    except Exception as inst:
        pass

    #and force a re-load
    xbmc.executebuiltin('Action(reloadkeymaps)')

    #and exit if requested
    if andexit:
        footprints(startup=False)


#called if we are running a playing instance...
def playInit():

    global xbmcAudioSuspended

    #Try and suspend XBMC's AudioEngine if it is present and has exclusive access to the audio device
    try:
        xbmc.audioSuspend();
        logNotice("Suspended XBMC AE")
        xbmcAudioSuspended = True
    except Exception as inst:
        logNotice("Unable to suspend XBMC AE: " + str(inst))
        pass

################################################################################
### MAIN

if ( __name__ == "__main__" ):

    xbmcAudioSuspended = False
    slaveProcess = None

    #log some tracks...
    footprints()
    logLocalIP()

    #pause
    if constants.SECONDS_TO_PAUSE_STARTUP!=0:
        logNotice("Pausing for " + str(constants.SECONDS_TO_PAUSE_STARTUP) + ", per request in XSqueeze settings.")
        notify("Pausing for " + str(constants.SECONDS_TO_PAUSE_STARTUP) + " seconds.", "(per request in XSqueeze settings.)")
        time.sleep(constants.SECONDS_TO_PAUSE_STARTUP)

    #is the add on configured yet?
    if constants.SERVERIP=="":

        #open the settings dialogue
        notify(LANGUAGE(19626), LANGUAGE(19631))
        constants.ADDON.openSettings()
        notify(LANGUAGE(19632),LANGUAGE(19633))
        cleanup()

    #Display the readme file if this is the users' first run of this version
    if constants.ISFIRSTRUN:
        log("First run of this version, so displaying FIRSTRUN.TXT then exiting...")
        viewer=ReadMeViewer()
        cleanup()
        #pass

    #not the first run...
    else:

        #serverIP still null, something went wrong...
        if constants.SERVERIP=="":
            notify(LANGUAGE(19624),LANGUAGE(19625))
            cleanup()

        #load our custom keymap to make sure that volume/skip track keys don't raise annoying xbmc messages
        #needed because xbmc addons can't swallow events
        #Each run we copy our keymap over, force xbmc to relaoad the keymaps, then at the end
        #we do the reverse - delete our custom one and reload the original setup
        try:
            shutil.copy(constants.KEYMAPSOURCEFILE, constants.KEYMAPDESTFILE)
            xbmc.executebuiltin('Action(reloadkeymaps)')
            logNotice("Installed custom keymap")
        except Exception as inst:
            logNotice("Error - couldn't copy & load custom keymap: " + str(inst))

        #are we running the locally installed Squeezeslave?
        if constants.PLAYBACK:

            #set up for actual playback - suspend AE as it can hog the audio device
            xbmcAudioSuspended = False
            playInit()

            logNotice("Starting local player [" + constants.PLAYERTYPE +"], system is [" + constants.SYSTEM + "]")
            notify(LANGUAGE(19608),LANGUAGE(19609))

            #builds the list ['/path/exefile','-arg1','-arg2',...]
            exe = constants.EXE
            args = constants.PLAYERARGS

            #add the new squeezelite -s switch for server if needed
            if constants.PLAYERTYPE == "squeezelite":
                args.append("-s")

            args.append(constants.SERVERIP)
            exe.extend(args)

            logNotice ("Attempting to start player: " + str(exe))
            logNotice ("Path is: " + str(sys.path))

            try:
                #need this to stop windows opening a console window
                if constants.SYSTEM.startswith("win"):
                    #for debugging, grab the process output....
                    #output, result = subprocess.Popen(exe, creationflags=0x08000000, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=False).communicate()
                    #log("Process Output is: " + str(output))
                    #log("Process Result is: " + str(result))
                    slaveProcess = subprocess.Popen(exe, creationflags=0x08000000, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=False)
                else:
                    #for debugging, grab the process output....
                    #output, result = subprocess.Popen(exe, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=False).communicate()
                    #log("$$$$$$$$$$$$$$$ " + str(output))
                    #log("$$$$$$$$$$$$$$$ " + str(result))
                    slaveProcess = subprocess.Popen(exe, shell=False)
            except Exception as inst:
                #Summat went wrong creating the player process...let's see if we can work out what!
                logNotice("Failed creating player process! ", inst)
                notify(LANGUAGE(19610),LANGUAGE(19611))
                #now let's try to start it again so we can log the output message for clues...
                if constants.SYSTEM.startswith("win"):
                    output, result = subprocess.Popen(exe, creationflags=0x08000000, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=False).communicate()
                else:
                    output, result = subprocess.Popen(exe, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=False).communicate()
                logNotice("ERROR RESULT: " + str(result))
                logNotice("ERROR OUTPUT: " + str(output))

                #...and bail out
                cleanup()

            pid = slaveProcess.pid
            logNotice("Process ID for player is "+ str(pid))

            #little pause to give player time to run & connect
            logNotice("Brief pause for dust to settle - " + str(constants.SECONDS_TO_PAUSE_CONNECT))
            time.sleep(1 + constants.SECONDS_TO_PAUSE_CONNECT)

        ##########################################################################
        # SETUP DONE > ON WITH THE SHOW

        #now let's make a window and see if we can send some commands...
        #check what skin to use
     
        #Gotham needs different skin files...
        version_stub = "_Frodo"
        if XBMC_VERSION == "Gotham":
            version_stub = ""

        try:
            if constants.PLAYERTYPE=="squeezelite":
                window = NowPlayingWindow("XSqueezeNowPlaying" + version_stub + ".xml",CWD,"Default")
            elif constants.TOUCHENABLED:
                window = NowPlayingWindow("XSqueezeNowPlaying" + version_stub + ".xml",CWD,"Default")
            else:
                window = NowPlayingWindow("XSqueezeNowPlaying_Slave" + version_stub + ".xml",CWD,"Default")

               #and kick this bad boy off....
            window.doModal()
        except:
            print_exc()

        ############################################################################
        # FINISHED (ONE WAY OR ANOTHER) - CLEAN UP!

        # after the window is closed, Destroy it.
        try:
            del window
        except:
            pass

        cleanup()


