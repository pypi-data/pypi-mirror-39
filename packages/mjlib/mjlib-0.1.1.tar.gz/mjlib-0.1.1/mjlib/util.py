import os
import sys
import time

import threading
import time
from os import system


if os.name == 'nt':
    import win32com.client as wincl
    import pythoncom


def println(s):
    print(s)

def write(s):
    sys.stdout.write(s)
    sys.stdout.flush()

# from gtts import gTTS
# from tempfile import TemporaryFile, NamedTemporaryFile

# utility functions


def thread(target, args=(), ):
    threading.Thread(target=target, args=args).start()


def daemon(target, args=(), ):
    threading.Thread(target=target, daemon=True, args=args).start()


is_profiling = False
last_profile_point = False
profile = []


# set a profile point. If profiling is on, this point will be included with the message s
def prof(s):
    if is_profiling:
        t = time.time()
        if len(profile) > 0:
            profile.append((t - profile[len(profile) - 1][2], s, t))
        else:
            profile.append((0, s, t))


# similar to prof(), but this is the starting or end point for a single profile
def main_prof(s):
    global last_profile_point, is_profiling
    if last_profile_point:
        prof(s)
        is_profiling = False
        last_profile_point = False
        print_prof()
        profile.clear()
    elif is_profiling:
        prof(s)
        last_profile_point = True


# print the results of a single profile to find out what sections of code are slowing down the algorithm
def print_prof():
    print('--------------------')
    print('\tprofile')
    print('--------------------')
    for t, s, unused in profile:
        print("{0:.1f}".format(t * 1000) + "\t" + s)
    print('--------------------')
    print('total: ' + str(profile[len(profile) - 1][2] - profile[0][2]))
    print('--------------------')


def append(file, s):
    with open(file, "a") as my_file:
        my_file.write(str(s))



def clear_file(file):
    with open(file, "w") as my_file:
        my_file.write("")


def appendln(file, s):
    append(file, s + "\n")


# from pygame import mixer
# mixer.init()

def say(s):
    s = str(s)
    print('saying: ' + s)
    if os.name == 'posix':
        system('say ' + s)
    elif os.name == 'nt':
        # tts = gTTS(text=s,lang='en')
        # f = NamedTemporaryFile()
        # tts.save(f.name)
        # mixer.music.load(f.name)
        # mixer.music.play()
        pythoncom.CoInitialize()
        speak = wincl.Dispatch("SAPI.SpVoice")
        speak.Speak(s)


def micros():
    return time.time() * 1000


