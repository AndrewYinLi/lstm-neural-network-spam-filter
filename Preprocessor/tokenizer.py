import glob
import fileinput
import os
import sys
from keras.preprocessing.text import Tokenizer
from keras.datasets import imdb
import pickle

def getFiles(inp, val):
	
	originalDir = os.getcwd()
	os.chdir(originalDir+'/stemmed')
	tokenFiles = [] # List of files to parse
	realFileNames = []
	openFiles = []
	for fileName in glob.glob(inp+"*"): # glob textfiles
		tokenFiles.append(fileName) # Add to list
		realFileNames.append(fileName[8:]) # Add real name to list
	for i in range(500):
		file = open(tokenFiles[i])
		openFiles.append(file.read())
		file.close()
	os.chdir(originalDir)
	with open(val+'_files.pickle', 'wb') as handle:
		pickle.dump(openFiles, handle, protocol=pickle.HIGHEST_PROTOCOL)
	return openFiles

def tokenize():
	tokenizer = Tokenizer()
	tokenFiles = [] # List of files to parse
	realFileNames = []
	openFiles = []
	counter = 0
	for fileName in glob.glob('./stemmed/*'): # glob textfiles
		tokenFiles.append(fileName) # Add to list
		realFileNames.append(fileName[8:]) # Add real name to list
    
	for fileName in tokenFiles:
		counter+=1;
		if counter%100 == 0:
			print(str(counter))
		file = open(fileName)
		openFiles.append(file.read())
		file.close()
	#print(openFiles[5])
	tokenizer.fit_on_texts(openFiles)
	with open('tokenizer.pickle', 'wb') as handle:
		pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
	return tokenizer
	#print(tokenFiles[0])
	#print(openFiles[0][:50])

def getTokenizer():
	#tokenizer = tokenize()
	with open('tokenizer.pickle', 'rb') as handle:
		tokenizer = pickle.load(handle)
	openFiles = getFiles()

	testText = 'from rssfeed @ jmason.org wed sep 25 10:24:03 2002'
	x = tokenizer.texts_to_sequences([testText, openFiles[5]])
	y = tokenizer.texts_to_sequences(openFiles)
	print(x[1])
	print(y[5])
	#print(tokenizer.word_counts)
	#print(x)

def main():
	
	hams = sys.argv[1]
	spams = sys.argv[2]
	tokenize()
	
	getFiles(spams, 'S')
	getFiles(hams, 'H')
	#(X_train, y_train), (X_test, y_test) = imdb.load_data()
	#print(X_train)

main()
