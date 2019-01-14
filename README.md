# AudioFormatDetective# AudioFormatDetective
Simple utility for reviewers
Uses audiotools and eyed3 to evaluate the attributes of audio files uploaded to the music library and checks them against the prerequisites. 
Prints [ok] or [ERROR] depending on how they evaluate. 

After feeding it hundreds of files, some valid, some corrupt, I think I've managed to catch most of the exceptions and allow it to keep chugging along happily.
