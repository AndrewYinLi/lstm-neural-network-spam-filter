# Andrew Yin Li | www.andrewyinli.com
# Use: arg1 = directory with stemmed emails, arg2 = train percentage, arg3 = seed

import glob
import fileinput
import sys
import os
import numpy as np
import random

from collections import Counter
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix 
from tqdm import tqdm

def splitSets(targetDirectory, trainingPercentage, seed):
	
	originalDirectory = os.getcwd() # Store current directory
	os.chdir(originalDirectory + '/' + targetDirectory) # Change to target directory

	allFiles = []
	for fileName in glob.glob('*.txt'): # glob textfiles
		fileNameSplit = fileName.split('_')
		if fileNameSplit[2] == 'stemmed': # Only add stemmed files | FOR DEBUG set index to 2, else set to 1
			allFiles.append(fileName)

	random.seed(seed)
	random.shuffle(allFiles)
	decimalTrainingPercentage = (int) (len(allFiles) * trainingPercentage) // 1
	train = allFiles[0:decimalTrainingPercentage]
	test = allFiles[decimalTrainingPercentage:len(allFiles)]


	# FOR DEBUG: Comment out block
	#for fileName in glob.glob('*.txt'):
	#	if fileName in train:
	#		os.rename(fileName, ('train_'+fileName))
	#	elif fileName in test:
	#		os.rename(fileName, ('test_'+fileName))

	os.chdir(originalDirectory) # Go back to original directory

	return len(train), len(test)


def getVocabulary(targetDirectory):

	originalDirectory = os.getcwd() # Store current directory
	os.chdir(originalDirectory + '/' + targetDirectory) # Change to target directory

	vocabulary = []
	for fileName in glob.glob('*.txt'): # glob textfiles
		fileNameSplit = fileName.split('_')
		if fileNameSplit[0] == 'train' and fileNameSplit[2] == 'stemmed': # Only add stemmed files
			emailFile = open(fileName, 'r', encoding="utf8", errors='ignore')
			for line in emailFile: # Add every word on each line in the file to our vocabulary
				vocabulary += line.split()
			emailFile.close()
	vocabulary = Counter(vocabulary) # Use built-in Python function to count occurrence of each word in doctionary format where word = key and occurrences = value
	vocabulary = vocabulary.most_common(2000)
	os.chdir(originalDirectory) # Go back to original directory
	print(vocabulary)
	return vocabulary


def getWordCounterVectorMatrix(targetDirectory, keyword, numEmails, vocabulary):
	
	originalDirectory = os.getcwd() # Store current directory
	os.chdir(originalDirectory + '/' + targetDirectory) # Change to target directory
	WCVMatrix = np.zeros((numEmails, len(vocabulary)))
	labels = np.zeros(numEmails)
	emailIndex = 0

	for fileName in tqdm(glob.glob('*.txt')): # glob textfiles
		fileNameSplit = fileName.split('_')
		if fileNameSplit[0] == keyword and fileNameSplit[2] == 'stemmed': # Only add stemmed files
			emailFile = open(fileName, 'r', encoding="utf8", errors='ignore')
			emailVocabulary = []
			for line in emailFile:
				lineSplit = line.split()
				emailVocabulary += lineSplit
			for emailVocab in emailVocabulary:
				wordIndex = 0;
				for i, vocab in enumerate(vocabulary):
					if vocab[0] == emailVocab:
						wordIndex = i
						WCVMatrix[emailIndex, wordIndex] = emailVocabulary.count(emailVocab)
			#for i, line in enumerate (emailFile):
			#	words = line.split()
			#	for word in words:
			#		wordIndex = 0
			#		for i, vocab in enumerate(vocabulary):
			#			if vocab[0] == word:
			#				wordIndex = i
			#				WCVMatrix[emailIndex, wordIndex] = words.count(word)
			emailFile.close()
			if fileNameSplit[1] == "ham":
				print("nice")
				labels[emailIndex] = 1
			emailIndex += 1
	os.chdir(originalDirectory) # Go back to original directory
	return WCVMatrix, labels



def main():

	targetDirectory = sys.argv[1]
	trainingPercentage = eval(sys.argv[2])
	seed = eval(sys.argv[3])

	trainLength, testLength = splitSets(targetDirectory, trainingPercentage, seed)
	vocabulary = getVocabulary(targetDirectory)
	
	trainWCVMatrix, trainLabels = getWordCounterVectorMatrix(targetDirectory, 'train', trainLength, vocabulary)
	naiveBayes = MultinomialNB()
	naiveBayes.fit(trainWCVMatrix, trainLabels)
	testWCVMatrix, testLabels = getWordCounterVectorMatrix(targetDirectory, 'test', testLength, vocabulary)
	result = naiveBayes.predict(testWCVMatrix)
	print(confusion_matrix(testLabels, result))

if  __name__ =='__main__':
	main()