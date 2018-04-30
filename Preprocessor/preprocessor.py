import StemmingUtil
import glob
import fileinput
import sys
import os

def main():

	originalDirectory = os.getcwd() # Store current directory
	os.chdir(originalDirectory + '/' + sys.argv[1]) # Change to target directory

	# Necessary precaution to create a list of files to parse as we will be creating new textfiles and don't want to parse those
	parseFiles = [] # List of files to parse
	for fileName in glob.glob('*.txt'): # glob textfiles
		parseFiles.append(fileName) # Add to list

	os.chdir(originalDirectory) # Go back to original directory

	stemmedDirectory = "stemmed"
	if not os.path.exists(stemmedDirectory): # Make a directory called stemmed if one doesn't exist
		os.makedirs(stemmedDirectory)

	# For each file in the list we just aggregated
	for fileName in parseFiles:
		allStems = [] # Array of arrays to keep track of list of stems for each line
		file = open(os.path.join(sys.argv[1], fileName), "r")
		for line in file:
			if not line.isspace(): # Get rid of white space
				words = StemmingUtil.parseTokens(line.lower()) # Parse into tokens
				stems = StemmingUtil.createStems(words) # Create stems
				allStems.append(stems) # Add to list of stems
		file.close()

		newFileName = sys.argv[1] + '_stemmed_' + fileName # Concatenate new file name
		file = open(os.path.join(stemmedDirectory, newFileName),'w') 

		for stems in allStems:
			stemLine = '' # WIll concatenate all stems for a line into this string
			for stem in stems:
				if stemLine != '': # Check if line is empty
					stemLine += ' '
				stemLine += stem # Append by default
			stemLine += '\n'
			file.write(stemLine)

		file.close()
				
if  __name__ =='__main__':
    main()