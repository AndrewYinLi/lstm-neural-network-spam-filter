# Long Short-Term Memory Neural Spam Filter

IF SOMETHING BREAKS, CONTANCT ali@oberlin.edu ASAP!

Contains 3 directories:

1. Preprocessor contains preprocessor.py, used to preprocess and stem the emails.

2. Naive Bayes contains nb.py, used to run Multinomial Naive Bayes

3. LSTM Neural Network contains tokenizer.py, used to tokenize stemmed emails and lstmnn.py, used to run the LSTM Neural Network.

## Getting Started

The spam and ham email corpus can be downloaded here: https://spamassassin.apache.org/old/publiccorpus/

We used spam and easy_ham. Convert all the files in the directories into .txt files! Also rename your spam directory to 'spam' and your ham directory to 'ham'. If something breaks, it's because you did not follow this critical step!

### Preprocessing

Preprocessor.py must be used twice, once on the ham directory and once on the spam directory. The stemmed files will go into a new directory called stemmed, which will be created if it does not already exist.

```
$ python preprocessor.py <ham/spam>

```

### Naive Bayes

Naive Bayes is simple to run, but requires that the 'stemmed' directory be deleted after each run of the program. If you would like to run nb.py again, you must perform the preprocessing step again.

The first argument should be 'stemmed', which is the directory that contains all the stemmed ham and spam files created by preprocessor.py, 0.75 is the recommended training percentage (75%), you can use any decimal number as a seed for splitting stemmed into a training and testing set.

```
$ python preprocessor.py stemmed <training percentage> <seed>

```

## Long Short-Term Memory Neural Network

While the folder containing the stemmed ham and spam emails is called 'stemmed', you will pass in 'ham' and 'spam' as arguments because the emails in 'stemmed' should be labeled as such automatically by preprocessor.py.

```
$ python tokenizer.py ham spam

```

Now that the pickle files have been created, you are ready to run the network! The network runs for 3 epochs and saves the resulting network into a .yaml file. Pass in '0' to run a fresh network and '1' to search for an existing .yaml network in the current directory, which allows you to stack series of 3 epochs onto the same network. You can use any decimal number as a seed for splitting stemmed into a training and testing set.

```
$ python lstmnn.py <0/1> <seed>

```


## Built With

Python and the Keras and scikit-learn libraries.


## Authors

* **Andrew Yin Li** - *Preprocessor and Naive Bayes*
* **Joshua Rappaport** - *LSTM Neural Network*
