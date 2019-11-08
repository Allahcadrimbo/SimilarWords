"""
Author: Grant Mitchell
Date: 11/6/19
PA #4 NLP CS 4242

In this PA we will be processing a directory of files to create a term x document matrix where each cell is a tf-idf
value, which we will use to determine the similarity between a pair of words entered by the user. For this PA we will
be doing some initial processing before calculating anything. In terms of processing we will make all of the text
lowercase, remove all non-alphanumerics, and we will remove all words that only occur once in the entire corpus
(not just one in a single document). It was mentioned above but we will be using the term frequency-inverse document
frequency or tf-idf measure. This measure is used to reflect how important a word is to a document in a collection of
documents. It is calculated as the product of two intuitions, term frequency and inverse document frequency. Term
frequency is the number of times word w occurs in document d. That is tf is the raw count of w in d. We can squash the
raw frequency by taking the log of the frequency instead. When we do this we add 1 to the raw frequency to avoid
taking the log of 0. The inverse document frequency is used to give a higher weight to words that occur only in a few
documents. The idf is defined with the fraction N/df_w, where N is the total number of documents and df_w is the number
documents the word w appears in. We can also squash this number with log. So the formula for tf-idf is as follows:
    tf-idf = log(count(w,d) + 1) * log(N/df_w)
Once we have all of these tf-idf values for every word in every document we can take a users pair of words and
calculate the cosine similarity between each words respective vector. Each words vector will be a list of their tf-idf
values for every document. Cosine similarity calculates the cosine of the angle between them, that is this will measure
the similarity of the orientation of between both vectors. The formula for cosine similarity is as follows:
    cos sim = (dot product of vector1 and vector 2)/(||vector 1|| * ||vector 2||)
This value (cos sim) is what will be returned to the user after entering their pair of words.

The following is example input and output:

input:
    python3 pa4.py path_to_dir_with_collection_of_documents

    PA 4 for CS 4242, written by Grant Mitchell. This program measures the similarity between pairs of words.

    Word 1: simply
    Word 2: audience

output:
    0.61065


Algorithm:
    - Variables/Data Structures that will be used throughout the algorithm
        - tf: This is a dict with word as the key and a list of its term frequency for each document as its value
            - tf = {"word": [freq 1, freq 2, ...], "word2": [freq 1, freq 2, ...]}
        - num_documents: This is an int counter that will keep track of the number of documents
        - df: A dict with the document frequency of each unique word in the entire corpus
            - df = {"word": frequency, "word2": frequency, ...}
        - tf_idf: A dict with each word as the key and a list of its tf-idf values for each document
    - Grab the path to the directory with the collection of documents
    - Call preprocess_data passing in the above directory as an argument
        - Iterate trough each file in the directory and open each file
            - For each file increment the document counter
            - With each open file read in the text and make it all lowercase and remove all non-alphanumerics
            - Iterate through each word in the file
                - Add each word to the list word_freq and the set df_set
            - For each word in df_set increment it's value in df
                - df_set will have each unique word in each document
        - Make a dict word_freq from Counter(word_freq)
            - This will return a dict with the frequency of every word in the corpus.
            - Make a temp dict and set it equal to the dict word_freq
            - Iterate through all of the words in the temp dict
                - If the frequency of word is 1, then remove it from the word_freq dict and df
        - Iterate through all of the files again and open them
            - For each word in the each file and it two a dict d where the key is the word and the value is the tf
                - Every time a word is encountered increment its tf
            - For each key in the dict word_freq
                - If key in dict d we add it to the words tf value list in dict tf
                - If key isn't in dict d we add 0 to the words tf value list in dict tf
    - Call calculate tf_idf_dict
        - For 0 to num_documents
            - Iterate through all of the keys in the word_freq dict
                - If the key is in the tf_idf dict
                    - Calculate the tf-idf value for the key and append it to tf_idf
                - Else calculate the tf-idf value for the key and add the key and the value to tf_idf
    - Prompt the user for a pair of words
        - Check that the words are in the corpus
        - Calculate the cosine similarity between the two words and return the result
"""
import sys
import os
import re
import math
from collections import Counter
from operator import mul

# Dictionary with the term frequency of each word
# tf = {"word": [freq 1, freq 2, ...]}
tf = dict()
# Counter for the number of documents in the corpus
num_documents = 0
# Document frequency for each word in the corpus
# df = {"word": frequency, "word2": frequency, ...}
df = dict()
# tf-idf values of each word for each document in the corpus
# tf_idf = {"word":['value 1', 'value 2'...]}
tf_idf = dict()
# List of all of the word in the corpus
word_freq = list()


# This function processes the dat and obtains the necessary information for latter calculations. This processing
# includes making all of the text lowercase, removing all non-alphanumerics, removing all words that only occur once in
# the corpus, getting the document frequency of each word, and getting the term frequency of each word.
# @param in_dir The directory with all of the files that we will be using as the corpus.
def preprocess_data(in_dir):
    global num_documents, tf, df, word_freq
    # Iterate through all of the files in the passed in directory
    for filename in os.listdir(in_dir):
        # Iterate the document counter for each new document
        num_documents = num_documents + 1
        # Open the current file
        with open(in_dir + "\\" + filename, "r") as infile:
            # Read in the file, make all of the text lowercase and remove all non-alphanumerics
            in_data = re.sub(r'[^a-zA-Z0-9\s]', '', infile.read().lower())  # Removes all non-alphanumerics
            in_data = re.sub(r'\s\s+', ' ', in_data)  # Removes the extra space created from the above line

            # This set will be used for each file to get a list of unique words in this document. Then this set will
            # be used to increment the document frequency of all of the words in this document
            df_set = set()

            # Iterate through each word in the files text
            for word in in_data.split():
                # Add every word to the word_freq list and df_set
                df_set.add(word)
                word_freq.append(word)

            # DF count
            # If the word is already in the df dict iterate it's counter by 1 else set add it and set it to 1.
            for word in df_set:
                if word in df:
                    df[word] = df[word] + 1
                else:
                    df[word] = 1

    # Makes a dict of every unique word in word_freq as the key and the frequency as the value
    word_freq = Counter(word_freq)
    # Need a temporary dictionary to use for the for loop because the size of word_freq will be changing as we iterate
    count_temp = dict(word_freq)
    # Iterate through all of the words and their frequencies. If the frequency is 1 then remove the word from both
    # word_freq and df. This for loop is removing all words that only occur once in the entire corpus
    for w, freq in count_temp.items():
        if freq == 1:
            del word_freq[w]  # Remove word from word_freq
            del df[w]  # Remove word from df

    # This for loop is going to get the term frequencies of each word in each document
    # Iterate through each file and open it
    for filename in os.listdir(in_dir):
        with open(in_dir + "\\" + filename, "r") as infile:
            # This dict will track the term freq of each word in the document
            d = dict()
            # Loop through each word in the file
            for word in infile.read().lower().split():
                # Check if the word is already in dictionary
                if word in d:
                    # Increment count of word by 1
                    d[word] = d[word] + 1
                else:
                    # Add the word to dictionary with count 1
                    d[word] = 1
            # Iterate through all of the words that we are considering post processing
            for word in word_freq.keys():
                # If that word is in the document add it to tf else add it tf as 0
                if word in d:
                    # Either append it to the tf[word] or add it if it doesn't exist already
                    if word in tf:
                        tf[word].append(d[word])
                    else:
                        tf[word] = [d[word]]
                else:
                    # Either append it to the tf[word] or add it if it doesn't exist already
                    if word in tf:
                        tf[word].append(0)
                    else:
                        tf[word] = [0]


# Creates the tf_idf dictionary. For each document it goes through every word and calculates the tf-idf value.
def calculate_tf_idf_dict():
    # From 0 to the number of documents in the corpus
    for i in range(num_documents):
        # word_freq has a list of every word in the corpus so go through every word
        for word in word_freq.keys():
            # If word is already in the tf_idf dictionary then append the new tf-idf value to the list of tf-idf values
            # for word
            if word in tf_idf:
                tf_idf[word].append(calculate_tf_idf(word, i))
            # If word isn't in the tf_dif dictionary add it and start a new list of tf_idf values for word
            else:
                tf_idf[word] = [calculate_tf_idf(word, i)]


# Calculates the tf-idf value of a word in a given document. For further info on tf-idf see block at the top.
# @param word The current word we are calculating tf-idf for
# @param index This is the current document index we are calculating for. ex. If index = 6 we will be calculating the
# tf-idf of word in regards to the seventh document
# @return The tf-idf value of word in the document index
def calculate_tf_idf(word, index):
    # The tf value is the raw count of the word freq in the specified document. We can squash the raw frequency a bit by
    # taking the log of the raw count. We add 1 to the log count avoid taking the log of 0.
    tf_value = math.log(tf[word][index] + 1)
    # The idf is the number of documents divided by the number of documents word appears in. This value can be squashed
    # as well by taking the log of it and we add one to avoid taking the log of 0.
    idf = math.log(num_documents / df[word])
    # Return the tf-idf value
    return tf_value * idf


# This function will calculate the cosine similarity between two words. For further def of cos sim see block at the top.
# @param w1 Word 1 given by the user
# @param w2 Word 2 given by the user
def calculate_cos_similarity(w1, w2):
    # Get the vectors of each word from the tf_idf dict
    v1 = tf_idf[w1]  # vector of word 1
    v2 = tf_idf[w2]  # vector of word 2
    # Calculate the dor product of the two vectors
    dot_prod = dot_product(v1, v2)
    # Calculate the magnitude of vector 1 and vector 2
    len1 = math.sqrt(dot_product(v1, v1))
    len2 = math.sqrt(dot_product(v2, v2))
    # Return the cosine sim
    return dot_prod / (len1 * len2)


# This function will calculate the dot product between two vectors
# @param v1 vector 1
# @param v2 vector 2
# @return The dot product of v1 and v2
def dot_product(v1, v2):
    # Map will iterate through all of the items in v1 and v2 and multiply them together. Then sum will add all of those
    # products together to give us the dot product of the two vectors v1 and v2.
    return sum(map(mul, v1, v2))


# This function checks if the two words passed in are in the corpus.
# @param w1 Word 1 that was inputted by the user
# @param w2 Word 2 that was inputted by the user
# @return True if they are both in the corpus else False.
def in_text_check(w1, w2):
    if w1 not in df or w2 not in df:
        return False
    else:
        return True


# This function prompts the user for a pair of words and then calculates their similarity. The similarity is returned
def prompt_user():
    print("PA 4 for CS 4242, written by Grant Mitchell. This program measures the similarity between pairs of words.")

    # Continue to prompt them for words until the stopping condition is met
    while True:
        word1 = input("Word 1: ")
        word2 = input("Word 2: ")

        # Stopping condition: If they enter "EXIT" for both words the while loop should end
        if word1 == "EXIT" and word2 == "EXIT":
            break

        # If one of the words in not in the corpus it will loop back to the top of the while and re-prompt them
        if not in_text_check(word1, word2):
            print("Not all words entered are in the corpus. Please try again")
            continue

        # Get the cosine similarity of the two words and format it so it is only 5 decimal places ex. 0.00005
        cos_sim = format(round(calculate_cos_similarity(word1, word2), 5))

        print(cos_sim)


if __name__ == "__main__":
    # sys.argv[1] is the command line argument of the
    preprocess_data(sys.argv[1])

    calculate_tf_idf_dict()

    prompt_user()
