import glob
import fileinput
from keras.preprocessing.text import Tokenizer

def main():
	tokenizer = Tokenizer(500)
	tokenFiles = [] # List of files to parse
	realFileNames = []
	openFiles = []
	for fileName in glob.glob('./spam/*'): # glob textfiles
		tokenFiles.append(fileName) # Add to list
		realFileNames.append(fileName[8:]) # Add real name to list
    
	for fileName in tokenFiles:
		file = open(fileName)
		openFiles.append(file.read())
		file.close()

	tokenizer.fit_on_texts(openFiles)
	print(tokenFiles[0])
	print(openFiles[0][:50])
	x = tokenizer.texts_to_matrix(openFiles, mode='count')
	y = 0
	for f in openFiles:
		print(realFileNames[y])
		print(x[y][:100])
		y+=1
	#print(tokenizer.word_counts)

main()
    
        
