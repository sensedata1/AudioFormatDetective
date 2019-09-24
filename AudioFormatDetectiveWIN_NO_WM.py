#!/usr/local/opt/python/libexec/bin/python
# Shebang for winbox #
import datetime
import logging
import os
import shutil
import time
from pathlib import Path
from zipfile import ZipFile
import eyed3
import speech_recognition as sr
from pydub import AudioSegment
import sys
import soundfile as sf
import wave
from send2trash import send2trash

# Let's define some colours
black = lambda text: '\033[0;30m' + text + '\033[0m'
red = lambda text: '\033[0;31m' + text + '\033[0m'
green = lambda text: '\033[0;32m' + text + '\033[0m'
yellow = lambda text: '\033[0;33m' + text + '\033[0m'
blue = lambda text: '\033[0;36m' + text + '\033[0m'
magenta = lambda text: '\033[0;35m' + text + '\033[0m'
cyan = lambda text: '\033[0;36m' + text + '\033[0m'
white = lambda text: '\033[0;37m' + text + '\033[0m'

# create global instance of speech_recognition
r = sr.Recognizer()


# Set up a "clear" with cross platform compatibility with Windows
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def unzip():
    os.chdir(AJDownloadsFolder)
    cwd = os.getcwd()
    # Look for zip files and unzip then remove
    for directory, subdirectories, files in os.walk(cwd):
        for file in files:
            # print(file) Debugging output
            if file.endswith((".zip", ".ZIP")) and os.path.isfile(os.path.join(directory, file)):
                currentZipFile = os.path.join(directory, file)
                zipFolderName = os.path.splitext(currentZipFile)[0]

                print(file)
                try:
                    with ZipFile(currentZipFile, 'r') as zipArchive:
                        try:
                            zipArchive.extractall(zipFolderName)
                            print('Extracting...')
                            print('Done!')
                            print("")
                            try:
                                zipArchive.close()
                                print("removing zipfile: " + currentZipFile)
                                os.remove(currentZipFile)
                            except Exception as e:
                                print(e)


                        except Exception as e:
                            # print("zip file corrupt")
                            print("Zip already extracted or corrupt")
                            print(e)

                        hiddenFolder = (os.path.join(zipFolderName, "__MACOSX"))
                        if os.path.isdir(hiddenFolder):
                            try:
                                shutil.rmtree(hiddenFolder)
                                print("Found and removed __MACOSX hidden folder...")
                                # print("")
                            except:
                                print("unable to remove __MACOSX hidden folder...")
                    return True

                except Exception as e:
                    print(e)
                    print("Unzip failed, zipfile may be corrupt")


def roundSeconds(dateTimeObject):
    newDateTime = dateTimeObject

    if newDateTime.microsecond >= 500000:
        newDateTime = newDateTime + datetime.timedelta(seconds=1)

    return newDateTime.replace(microsecond=0)


def process_audio_files(currentFile):
    # currentFile = fileList
    eyed3.log.setLevel("ERROR")
    curPath, file = os.path.split(currentFile)

    if currentFile.endswith((".mp3", ".MP3", ".Mp3")) and not currentFile.startswith(".") \
            and os.path.isfile(currentFile):
        try:
            mp3File = eyed3.load(currentFile)
        except:
            mp3File = "Could not load MP3"
        try:
            bitRate = mp3File.info.bit_rate
        except:
            bitRate = ""
        try:
            sampleRate = mp3File.info.sample_freq
        except:
            sampleRate = "Samplerate Unsupported"
        try:
            channels = str(mp3File.info.mode)
        except:
            channels = ""
        try:
            durationSecs = mp3File.info.time_secs
            duration2 = str(datetime.timedelta(seconds=durationSecs))
            duration = duration2.split(".")[0]
        except:
            duration = "***"
        # try:
        #     bits = (audiotools.open(currentFile).bits_per_sample())
        # except:
        bits = "  "

        # convert mp3 to wav for voice recognition
        # home = str(Path.home())
        # src = currentFile
        # dst = os.path.join(home, "tempWav.wav")
        # # convert wav to mp3
        # sound = AudioSegment.from_mp3(src)  # [10000:]
        # sound.export(os.path.join(home, "tempWav.wav"), format="wav")
        # # Do watermark detection with voice recognition only on testWav.wav
        # srVoiceTestWav = sr.AudioFile(dst)
        # try:
        #     with srVoiceTestWav as source:
        #
        #         audio = r.record(source, duration=10)
        #
        #         recognisedSpeech = str((r.recognize_google(audio)))
        #         if recognisedSpeech.find("jungle") is not -1:
        #             ch = red("WM")
        #         elif recognisedSpeech.find("audio") is not -1:
        #             ch = red("WM")
        #         elif "jungle" in str(recognisedSpeech):
        #             ch = red("WM")
        #         elif "Jungle" in str(recognisedSpeech):
        #             ch = red("WM")
        #         elif "audiojungle" in str(recognisedSpeech):
        #             ch = red("WM")
        #         elif recognisedSpeech.find("audiojungle") is not -1:
        #             ch = red("WM")
        #         else:
        #             ch = "  "
        # except Exception as e:
        ch = "  "
        #     wm = "nowm"
        recognisedSpeech = ''

        if channels == "Joint stereo" or "Stereo" or "stereo" or "Joint Stereo":
            channels = 2
        try:
            rate = int(bitRate[1])
        except:
            rate = "err"
        vbrTrueFalse = "  "
        if sampleRate == 44100 and channels == 2 and rate < 325 and rate > 315:  # and wm != "wmd":
            errorMp3 = green(" [ok]")
        else:
            errorMp3 = red("[ERR]")
        ######################################################################################
        #           PRINT MP3 DATA                                                           #
        ######################################################################################
        ch = "ch"
        print(errorMp3, sampleRate, bits, channels, ch, vbrTrueFalse, rate, duration[3:], file, red(recognisedSpeech))
    # Look for wav files and evaluate
    if currentFile.endswith((".wav", ".WAV", ".WaV", ".wAV", ".WAv", ".Wav")) and not currentFile.startswith(".") \
            and os.path.isfile(currentFile):
        ob = wave.open(currentFile, mode='r')
        try:
            sampleRate = ob.getframerate()
            ch = "ch"
            gap = "      "
        except:
            sampleRate = "Samplerate unsupported"
            gap = ""
            ch = ""
        try:
            ob2 = sf.SoundFile(currentFile)
            subtype = ob2.subtype
            pre_bits = str(subtype[-2:])
            bits = int(pre_bits)
        except:
            bits = ""
        try:
            channels = ob.getnchannels()
        except:
            channels = ""
            # try:
            #     home = str(Path.home())
            #     LACpath = os.path.join(home, "LAC")
            #     a = [LACpath, currentFile]
            #
            #     p = subprocess.Popen(a, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            #     p2 = subprocess.Popen(['grep', 'Result'], stdin=p.stdout,
            #                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #     sys.stdout.flush()
            #     for line in iter(p2.stdout.readline, b''):
            #         LACout = str(line)
            # except Exception as ex:
            #     print("crap!")
            #     print(ex)
            LACout = ''
        try:

            frames = ob.getnframes()
            rate = ob.getframerate()
            durationSecsWav = frames / float(rate)

            duration2 = str(datetime.timedelta(seconds=durationSecsWav))
            duration = duration2.split(".")[0]
        except:
            duration = "****"
        # srVoiceTestWav = sr.AudioFile(currentFile)
        # try:
        #     with srVoiceTestWav as source:
        #         audio = r.record(source, duration=10)
        #
        #         recognisedSpeech = str((r.recognize_google(audio)))
        #         if recognisedSpeech.find("jungle") is not -1:
        #             ch = red("WM")
        #         elif recognisedSpeech.find("audio") is not -1:
        #             ch = red("WM")
        #         elif "jungle" in str(recognisedSpeech):
        #             ch = red("WM")
        #         elif "Jungle" in str(recognisedSpeech):
        #             ch = red("WM")
        #         elif "audiojungle" in str(recognisedSpeech):
        #             ch = red("WM")
        #         elif recognisedSpeech.find("audiojungle") is not -1:
        #             ch = red("WM")
        #         else:
        #             ch = "  "
        # except Exception as e:
        #
        #     ch = "  "
        recognisedSpeech = ''
        if sampleRate == 44100 and bits == 16 and channels == 2:  # and wm !="wmd":
            errorWav = green(" [ok]")
        else:
            errorWav = red("[ERR]")
            LACout = ""

        ######################################################################################
        #           PRINT WAV DATA                                                           #
        ######################################################################################
        print(errorWav, sampleRate, bits, channels, ch, gap, duration[3:], file, red(recognisedSpeech))
    # If any other audio file types are present mark as [ERR]
    if file.endswith((".aac", ".aiff", ".aif", ".flac", ".m4a", ".m4p")) \
            and os.path.isfile(currentFile):
        # currentFile = os.path.join(directory, file)
        try:
            sampleRate = "Not a WAV file"
        except:
            sampleRate = "Samplerate Unsupported"
        try:
            bits = " "
        except:
            bits = " "
        try:
            channels = " "
        except:
            channels = " "
        errorWav = red("[ERR]")
        ch = ""
        print(errorWav, sampleRate, bits, channels, ch, "         ", file)


def os_walk():
    # print(event)
    os.chdir(AJDownloadsFolder)
    cwd = os.getcwd()
    if unzip():

        clear()
        print('\n' * 50)
        print("analysing...")
        time.sleep(1)
        currentFileList = []

        for directory, subdirectories, files in os.walk(cwd):
            for file in files:
                tempCurrentFile = os.path.join(directory, file)
                if tempCurrentFile.endswith \
                            ((".mp3", ".MP3", ".Mp3", ".aac",
                              ".aiff", ".aif", ".flac", ".m4a",
                              ".m4p", ".wav", ".WAV", ".WaV",
                              ".wAV", ".WAv", ".Wav")) and not tempCurrentFile.startswith(".") \
                        and os.path.isfile(tempCurrentFile):
                    currentFileList.append(tempCurrentFile)

        for currentFile in currentFileList:
            process_audio_files(currentFile, )

        print("All done!")


if __name__ == "__main__":
    # Suppress warnings from eyeD3
    eyed3.log.setLevel("ERROR")
    # Get AJ Downloads folder from user input
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    userFolder = input("Drag your AJ downloads folder here and hit enter a couple of times..")
    tempDir = Path(userFolder)
    print(tempDir)
    # Format the user input
    # tempVar = userFolder.replace("\\", "")
    # tempVar2 = tempVar.rstrip()
    AJDownloadsFolder = tempDir
    # AJDownloadsFolder = os.path.dirname(tempVar2)

    os.chdir(AJDownloadsFolder)
    print("Downloads folder = " + str(tempDir))
    print("")
    print("Monitoring " + str(tempDir) + "...")

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'

    try:
        while True:
            time.sleep(1)
            os_walk()

    except KeyboardInterrupt:
        print("Interrupt received, stopping...")
    finally:
        exit()
