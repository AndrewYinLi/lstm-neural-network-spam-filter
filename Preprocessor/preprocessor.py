# Andrew Yin Li | www.andrewyinli.com
# Use: Pass target directory as an argument

import StemmingUtil
import glob
import fileinput
import sys
import os
import re

def main():

	originalDirectory = os.getcwd() # Store current directory
	os.chdir(originalDirectory + '/' + sys.argv[1]) # Change to target directory

	# Necessary precaution to create a list of files to parse as we will be creating new textfiles and don't want to parse those
	parseFiles = [] # List of files to parse
	for fileName in glob.glob('*.txt'): # glob textfiles
		parseFiles.append(fileName) # Add to list

	os.chdir(originalDirectory) # Go back to original directory

	stemmedDirectory = 'stemmed'
	if not os.path.exists(stemmedDirectory): # Make a directory called stemmed if one doesn't exist
		os.makedirs(stemmedDirectory)


	regex = re.compile('[^0-9a-zA-Z]') # Regex of what we want

	# For each file in the list we just aggregated
	for fileName in parseFiles:
		allStems = [] # Array of arrays to keep track of list of stems for each line
		emailFile = open(os.path.join(sys.argv[1], fileName), 'r', encoding="utf8", errors='ignore')
		for line in emailFile:
			if not line.isspace(): # Get rid of white space

				words = StemmingUtil.parseTokens(re.sub('[^0-9A-Za-z ]+', '', line.lower())) # Parse into tokens
				stems = StemmingUtil.createStems(words) # Create stems
				allStems.append(stems) # Add to list of stems
		emailFile.close()

		newFileName = sys.argv[1] + '_stemmed_' + fileName # Concatenate new file name
		emailFile = open(os.path.join(stemmedDirectory, newFileName),'w', encoding="utf8", errors='ignore') 

		for stems in allStems:
			stemLine = '' # WIll concatenate all stems for a line into this string
			for stem in stems:
				if stemLine != '': # Check if line is empty
					stemLine += ' '
				stemLine += stem # Append by default
			stemLine += '\n'
			emailFile.write(stemLine)

		emailFile.close()
				
if  __name__ =='__main__':
    main()