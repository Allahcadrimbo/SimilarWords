# SimilarWords
PA #4 NLP CS 4242

## Description
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
documents the word w appears in. We can also squash this number with log. So the formula for tf-idf is as follows:\
\
    tf-idf = log(count(w,d) + 1) * log(N/df_w)\
\
Once we have all of these tf-idf values for every word in every document we can take a users pair of words and
calculate the cosine similarity between each words respective vector. Each words vector will be a list of their tf-idf
values for every document. Cosine similarity calculates the cosine of the angle between them, that is this will measure
the similarity of the orientation of between both vectors. The formula for cosine similarity is as follows:
    cos sim = (dot product of vector1 and vector 2)/(||vector 1|| * ||vector 2||)
This value (cos sim) is what will be returned to the user after entering their pair of words.

## Example Input and Output
The following is example input and output:\
input:\
    `python3 pa4.py <path_to_dir_with_collection_of_documents>`\
    PA 4 for CS 4242, written by Grant. This program measures the similarity between pairs of words.\
    Word 1: simply\
    Word 2: audience\
output:
    0.61065
    
## Algorithm
Algorithm:\
    &emsp;- Variables/Data Structures that will be used throughout the algorithm\
        &emsp;&emsp;- tf: This is a dict with word as the key and a list of its term frequency for each document as its value\
            &emsp;&emsp;&emsp;- tf = {"word": [freq 1, freq 2, ...], "word2": [freq 1, freq 2, ...]}\
        &emsp;&emsp;- num_documents: This is an int counter that will keep track of the number of documents\
        &emsp;&emsp;- df: A dict with the document frequency of each unique word in the entire corpus\
            &emsp;&emsp;&emsp;- df = {"word": frequency, "word2": frequency, ...}\
        &emsp;&emsp;- tf_idf: A dict with each word as the key and a list of its tf-idf values for each document\
    &emsp;- Grab the path to the directory with the collection of documents\
    &emsp;- Call preprocess_data passing in the above directory as an argument\
        &emsp;&emsp;- Iterate trough each file in the directory and open each file\
            &emsp;&emsp;&emsp;- For each file increment the document counter\
            &emsp;&emsp;&emsp;- With each open file read in the text and make it all lowercase and remove all non-alphanumerics\
            &emsp;&emsp;&emsp;- Iterate through each word in the file\
                &emsp;&emsp;&emsp;&emsp;- Add each word to the list word_freq and the set df_set\
            &emsp;&emsp;&emsp;- For each word in df_set increment it's value in df\
                &emsp;&emsp;&emsp;&emsp;- df_set will have each unique word in each document\
        &emsp;&emsp;- Make a dict word_freq from Counter(word_freq)\
            &emsp;&emsp;&emsp;- This will return a dict with the frequency of every word in the corpus.\
            &emsp;&emsp;&emsp;- Make a temp dict and set it equal to the dict word_freq\
            &emsp;&emsp;&emsp;- Iterate through all of the words in the temp dict\
                &emsp;&emsp;&emsp;&emsp;- If the frequency of word is 1, then remove it from the word_freq dict and df\
        &emsp;&emsp;- Iterate through all of the files again and open them\
            &emsp;&emsp;&emsp;- For each word in the each file and it two a dict d where the key is the word and the value is the tf\
                &emsp;&emsp;&emsp;&emsp;- Every time a word is encountered increment its tf\
            &emsp;&emsp;&emsp;- For each key in the dict word_freq\
                &emsp;&emsp;&emsp;&emsp;- If key in dict d we add it to the words tf value list in dict tf\
                &emsp;&emsp;&emsp;&emsp;- If key isn't in dict d we add 0 to the words tf value list in dict tf\
    &emsp;- Call calculate tf_idf_dict\
        &emsp;&emsp;- For 0 to num_documents\
            &emsp;&emsp;&emsp;- Iterate through all of the keys in the word_freq dict\
                &emsp;&emsp;&emsp;&emsp;- If the key is in the tf_idf dict\
                    &emsp;&emsp;&emsp;&emsp;&emsp;- Calculate the tf-idf value for the key and append it to tf_idf\
                &emsp;&emsp;&emsp;&emsp;- Else calculate the tf-idf value for the key and add the key and the value to tf_idf\
    &emsp;- Prompt the user for a pair of words\
        &emsp;&emsp;- Check that the words are in the corpus\
        &emsp;&emsp;- Calculate the cosine similarity between the two words and return the result\
