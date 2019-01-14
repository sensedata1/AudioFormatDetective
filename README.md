# AudioFormatDetective# AudioFormatDetective
Simple utility for reviewers
Uses audiotools and eyed3 to evaluate the attributes of audio files uploaded to the music library and checks them against the prerequisites. 
Prints [ok] or [ERROR] depending on how they evaluate. 

After feeding it hundreds of files, some valid, some corrupt, I think I've managed to catch most of the exceptions and allow it to keep chugging along happily.

Requires
 audiotools
 eyeD3
 zipFile

Note, This won't be of much use to many folks as it is as this is looking for
WAV files with the following spec:

44100kHz sample frequency
16bits per sample
Stereo channels			

and MP3 files with the following spec:

444100 sample frequency
16bits per sample
320kbps cbr bitrate

Although it's easily modified.

The onefile dist runs fine on my Mac

	
