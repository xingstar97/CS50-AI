import nltk
import sys
import os
import string
import math
from collections import Counter
# nltk.download('stopwords')

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    for file in os.listdir(directory):
        with open(os.path.join(directory, file), errors = "ignore") as f:
            files[file] = f.read().replace("\n", " ")
    return files

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = list()
    # for word in nltk.word_tokenize(document):
    #     if not word in string.punctuation and not word in nltk.corpus.stopwords.words("english"):
    #         words.append(word.lower())
    words.extend([
        word.lower() for word in nltk.word_tokenize(document)
        if not word in string.punctuation and
        not word in nltk.corpus.stopwords.words("english")
    ])
    return sorted(words)


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    total = len(documents)
    idfs = dict()
    words = set()
    for file in documents:
        words.update(documents[file])
    for word in words:
        count = 0
        for file in documents:
            if word in documents[file]:
                count +=1
        idfs[word] = math.log(total/count)
    return idfs    


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    output = dict()
    for word in query:
        if word in idfs:
            idf = idfs[word]
        else:
            continue
        for file in files:
            tfs = Counter(files[file])
            tf = tfs[word]
            if file not in output:
                output[file] = tf * idf
            else:
                output[file] += tf * idf
    unsorted = list()
    for file in output:
        unsorted.append(file)
    return sorted(unsorted, key = lambda t:output[t], reverse = True)[:n]

            



def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    output = dict()
    qtd = dict()
    for word in query:
        for sentence in sentences:
            if word in sentences[sentence]:
                if sentence not in output:
                    output[sentence] = idfs[word]
                    qtd[sentence] = 1
                else:
                    output[sentence] += idfs[word]
                    qtd[sentence] +=1
    unsorted = list()
    for sentence in output:
        unsorted.append(sentence)
    return sorted(unsorted, key = lambda t:(output[t], qtd[t]/len(sentences[t])), reverse = True)[:n]
    


if __name__ == "__main__":
    main()
