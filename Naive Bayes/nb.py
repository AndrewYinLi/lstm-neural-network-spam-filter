# Andrew Yin Li | www.andrewyinli.com
# Use: arg1 = directory with stemmed emails, arg2 = train percentage, arg3 = seed

import glob
import fileinput
import sys
import os
import numpy as np
import time
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
		if fileNameSplit[1] == 'stemmed': # Only add stemmed files | FOR DEBUG set index to 2, else set to 1
			allFiles.append(fileName)

	random.seed(seed)
	random.shuffle(allFiles)
	decimalTrainingPercentage = (int) (len(allFiles) * trainingPercentage) // 1
	train = allFiles[0:decimalTrainingPercentage]
	test = allFiles[decimalTrainingPercentage:len(allFiles)]


	# FOR DEBUG: Comment out block
	for fileName in glob.glob('*.txt'):
		if fileName in train:
			os.rename(fileName, ('train_'+fileName))
		elif fileName in test:
			os.rename(fileName, ('test_'+fileName))

	os.chdir(originalDirectory) # Go back to original directory

	return len(train), len(test)

def getVocabulary(targetFile):
	textFile = open(targetFile, 'r', encoding="utf8", errors='ignore')
	vocabulary = []
	for line in textFile:
		vocabulary += line.split()
	textFile.close()
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
			emailVocabulary = getVocabulary(fileName)
			for emailVocab in emailVocabulary:
				matrixIndex = 0
				for vocab in vocabulary:
					if vocab[0] == emailVocab:
						WCVMatrix[emailIndex, matrixIndex] = emailVocabulary.count(emailVocab)
					matrixIndex += 1
			if fileNameSplit[1] == "ham":
				labels[emailIndex] = 1
			emailIndex += 1
	os.chdir(originalDirectory) # Go back to original directory
	return WCVMatrix, labels



def main():
	timeStart = time.time() # Initial time

	targetDirectory = sys.argv[1]
	trainingPercentage = eval(sys.argv[2])
	seed = eval(sys.argv[3])

	trainLength, testLength = splitSets(targetDirectory, trainingPercentage, seed)

	# Generate vocabulary
	originalDirectory = os.getcwd() # Store current directory
	os.chdir(originalDirectory + '/' + targetDirectory) # Change to target directory

	vocabulary = []
	for fileName in glob.glob('*.txt'): # glob textfiles
		fileNameSplit = fileName.split('_')
		if fileNameSplit[0] == 'train' and fileNameSplit[2] == 'stemmed': # Only add stemmed files
			emailVocabulary = getVocabulary(fileName)
			#for emailVocab in emailVocabulary:
			vocabulary += emailVocabulary
	vocabulary = Counter(vocabulary).most_common(2000) # Use built-in Python function to count occurrence of each word in dictionary format where word = key and occurrences = value and then take the 2000 greatest
	os.chdir(originalDirectory) # Go back to original directory
	
	naiveBayes = MultinomialNB()
	trainWCVMatrix, trainLabels = getWordCounterVectorMatrix(targetDirectory, 'train', trainLength, vocabulary)
	naiveBayes.fit(trainWCVMatrix, trainLabels)
	testWCVMatrix, testLabels = getWordCounterVectorMatrix(targetDirectory, 'test', testLength, vocabulary)
	result = naiveBayes.predict(testWCVMatrix)
	print(confusion_matrix(testLabels, result))
	print("Time elapsed: "+str(time.time() - timeStart))

if  __name__ =='__main__':
	main()