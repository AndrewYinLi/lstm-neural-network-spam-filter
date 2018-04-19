import StemmingUtil
import glob
import fileinput

def main():

	# Necessary precaution to create a list of files to parse as we will be creating new textfiles and don't want to parse those
	parseFiles = [] # List of files to parse
	for fileName in glob.glob('*.txt'): # glob textfiles
		parseFiles.append(fileName) # Add to list

	# For each file in the list we just aggregated
	for fileName in parseFiles:
		allStems = [] # Array of arrays to keep track of list of stems for each line
		file = open(fileName)
		for line in file:
			if not line.isspace(): # Get rid of white space
				words = StemmingUtil.parseTokens(line.lower()) # Parse into tokens
				stems = StemmingUtil.createStems(words) # Create stems
				allStems.append(stems) # Add to list of stems
		file.close()

		newFileName = 'stemmed_' + fileName # Concatenate new file name
		file = open(newFileName,'w') 

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