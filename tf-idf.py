"""
This script takes in a directory/folder of "m" .txt files and generates a mxn tf-idf matrix, where each row is a document in
the directory, and each column is a word.

This code was based off of Ayasdi's patent for metric smoothing.

"""

import os
import sys
import re
import math
import optparse
import logging
import numpy
import scipy
import pandas as pd

"""
Change path to directory as you need. Make sure all files are
.txt files in that directory.

"""
# declaring a path to the texts
path = 'path\\to\\directory'

# number of files in the directory
num_files = len(os.listdir(path))

# initialize empty bag of words list
BoW = []

# initialize empty list of filenames
filenames = []

# creating a list of lists:
for i in range(0, num_files):
    BoW.append([])

# opening .txt files in the above directory
for filename in os.listdir(path):
    filenames.append(filename)

# creating a list of bag of words for each document in the corpus
for i in range(0, num_files):
    filename = filenames[i]

    # path to file
    filepath =path+filename

    # open the file in Python
    openfile = open(filepath, 'r')

    """
    First, we return each document in an appropriately formated manner.

    For this, we first tokenize the document, and store each document
    as a "bag of words" in the i'th BOW list.

    """
    # convert the open file to lower case.
    text = openfile.read().lower()
    openfile.close()

    # use the re module to replace all non-"a-z" characters with " "
    text = re.sub('[^a-z\ \']+', " ", text)

    # add words to the i'th Bag of Words (list)
    BoW[i] =  list(text.split())

"""
We now have a set of "Bag of Words" for each document
in out corpus. Each document, is thus, tokenized. In order to
convert these tokenized BoW documents to numbers, a simple
strategy would be to create a vector of all possible words, and to
then count the occurences of each word in the document.

"""

# initialize set of words
corpusDict = set({})

# iterate over our bag of words list to create a dictionary
for i in range(0, num_files):
    corpusDict = corpusDict.union(set(BoW[i]))

"""
We are also going to need the number of occurances
of each word in corpusDict in each bag of words.
The following code does exactly that.

"""

# initialize an empty list to store dictionaries of word-occurances
# for each word in the corpus
corpusDocDict = []

# initialize 0-valued dicts for each document in the corpus
for i in range(0, num_files):
    corpusDocDict.append(dict.fromkeys(corpusDict, 0))

# set up correct values of words in each document
# using a nested loop as follows
for i in range(0, num_files):
    for word in BoW[i]:
        corpusDocDict[i][word]+=1
"""
We thus have a dictionary for each document in the corpus with the number
of occurrances of each word in the corpuss in each document.

"""
wordMatrix = pd.DataFrame([corpusDocDict[i] for i in range(0, num_files)])

"""
However, there are a few significant advantages to using the tf-idf
matrix formulation (described in my write-up). Following code allows you to generate
a tf-idf matrix.

"""

def TF(doc_dictionary, bag_of_words):
    tfDict = {}
    bowCount = len(bag_of_words)
    for word, count in doc_dictionary.items():
        tfDict[word] = count/float(bowCount)
    return tfDict

def IDF(filenames):
    idfDict = {}
    idfDict = dict.fromkeys(corpusDict, 0)
    for i in range(0, num_files):
        filename = filenames[i]
        filepath =path+filename
        openfile = open(filepath, 'r')
        for word, val in corpusDocDict[i].items():
            if val > 0:
                idfDict[word] +=1
    for word, val in idfDict.items():
        idfDict[word]= math.log(num_files / float(val))
    return idfDict

# TODO define alternative TFIDF measures based on alternative
# tf values.

def TFIDF(tfbow, idfs):
    tfidf = dict({})
    for word, val in tfbow.items():
        tfidf[word] = val * idfs[word]
    return tfidf

# We now generate the tfBoWs and the idfs.

tfBoWs = []
for i in range(0, num_files):
    tfBoWs.append(TF(corpusDocDict[i], BoW[i]))

idfs = IDF(filenames)

tfidf = []
for i in range(0, num_files):
    tfidf.append(TFIDF(tfBoWs[i], idfs))

TFIDF_matrix = pd.DataFrame([tfidf[i] for i in range(0, num_files)])

# TO DO: NEED TO INSERT AN EMPTY FIRST CELL IN THIS ROW OF WORDS.
#row_of_words = pd.DataFrame([dict.fromkeys(corpusDict, 0)])

column_of_doc_names = pd.DataFrame((filenames[i] for i in range(0, num_files)))

# Add a column with the names of documents, makes it easier to track after TDA. 
final = pd.concat([column_of_doc_names, TFIDF_matrix], axis=1)


def smooth(matrix):
    threshold = 0.001

    for word in matrix.columns:
            
            num_significant = 0

            column = matrix[word]
            for freq in column:
                if freq > threshold:
                    num_significant += 1
            if num_significant <= 1:
                
                del column;

    print(matrix)


final.to_csv('LARGE', index=False, header=False)
final.to_csv('name_of_csv_file', index=False, header=False)
