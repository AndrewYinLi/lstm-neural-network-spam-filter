###############################
# rnn.py
# Joshua Rappaport
#
# Certain bits of code taken from https://machinelearningmastery.com/sequence-classification-lstm-recurrent-neural-networks-python-keras/
###############################

import pickle
import numpy
import glob
import copy
import random
import sys
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.models import model_from_yaml
from sklearn import metrics
from sklearn.metrics import confusion_matrix

random.seed(42) #set the same random seed to reproducing results

def shffl(x,y):
    assert len(x) == len(y)
    state = random.getstate()
    random.shuffle(x)
    random.setstate(state)
    random.shuffle(y)

#test code used to obtain files.
def getFiles():
	tokenFiles = [] # List of files to parse
	realFileNames = []
	openFiles = []
	for fileName in glob.glob('./preprocessor/original/stemmed/S_*'): # glob textfiles
		tokenFiles.append(fileName) # Add to list
		realFileNames.append(fileName[8:]) # Add real name to list
	for fileName in tokenFiles:
		file = open(fileName)
		openFiles.append(file.read())
		file.close()
	with open('S_files.pickle', 'wb') as handle:
		pickle.dump(openFiles, handle, protocol=pickle.HIGHEST_PROTOCOL)

#Build the model
def makeModel(vocab_len, input_len):
    embedding_vector_length = 32
    
    model = Sequential()
    model.add(Embedding(vocab_len, embedding_vector_length, input_length=input_len))
    model.add(LSTM(300))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

#Build test and train set from the two unpickled files.
def makeSets(tokenizer, S, H):
    S_tokenized = tokenizer.texts_to_sequences(S)
    H_tokenized = tokenizer.texts_to_sequences(H)

    S_len = len(S_tokenized)
    H_len = len(H_tokenized)
    S_train_len = int(S_len*3/4)
    H_train_len = int(H_len*3/4)
    S_test_len = S_len - S_train_len
    H_test_len = H_len - H_train_len
    
    X_train = copy.deepcopy(S_tokenized[0:S_train_len]) + \
              copy.deepcopy(H_tokenized[0:H_train_len])
    Y_train = ([0]*S_train_len)+([1]*H_train_len)
    X_test = copy.deepcopy(S_tokenized[S_train_len:]) + \
             copy.deepcopy(H_tokenized[H_train_len:])
    Y_test = ([0]*S_test_len)+([1]*H_test_len)

    shffl(X_train, Y_train)
    #shffl(X_test, Y_test)
    
    return (X_train, Y_train), (X_test, Y_test)

def save(model):
    model_yaml = model.to_yaml()
    with open("model.yaml", "w") as yaml_file:
        yaml_file.write(model_yaml)
    model.save_weights("model.h5")
    print("Saved the model to model.yaml and model.h5!")

def load():
    yaml_file = open("model.yaml", "r")
    loaded_model_yaml = yaml_file.read()
    yaml_file.close()
    model = model_from_yaml(loaded_model_yaml)
    model.load_weights("model.h5")
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    print("Loaded model from model.yaml and model.h5!")
    return model

def main():
    #load up the tokenizer and the non-tokenized files
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    with open('S_files.pickle', 'rb') as handle:
        S = pickle.load(handle)
    with open('H_files.pickle', 'rb') as handle:
        H = pickle.load(handle)
        
    #Set some parameters
    vocab_length = len(tokenizer.word_index)+1
    max_email_length = 1500

    #make the input
    (X_train, Y_train), (X_test, Y_test) = makeSets(tokenizer, S, H)
    X_train = sequence.pad_sequences(X_train, maxlen=max_email_length)
    X_test = sequence.pad_sequences(X_test, maxlen=max_email_length)

    print(vocab_length)

    #make the model
    if (sys.argv[1] == '1'):
        model = load()
    else:
        model = makeModel(vocab_length, max_email_length)

    assert len(X_test) == len(Y_test)

    #DO THE THING!!!!
    print(model.summary())
    model.fit(X_train, Y_train, epochs=3, batch_size=32)

    #Test the thing and show results!
    scores = model.evaluate(X_test, Y_test)
    print("Accuracy: %.2f%%" % (scores[1]*100))
    #print(scores)
    predictions = model.predict_classes(X_test, 32, 1)
    #print(predictions)
    cf = metrics.confusion_matrix(Y_test, predictions)
    print(cf)

    #Save the model!
    save(model)

main()
    
