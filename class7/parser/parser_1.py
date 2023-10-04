import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> S Conj S | NP VP | S Conj VP
NP -> N | Det N | Det AP N | AP N | NP PP
VP -> V | Adv VP | V PP | V NP | VP Adv
PP -> P NP 
AP -> Adj | Adj AP

"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e) 
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = []
    # parsed = nltk.word_tokenize(sentence)
    # for word in parsed:
    #     for c in word:
    #         if c.isalpha():
    #             words.add(word.lower())
    # return list(words)
    words.extend([
        word.lower() for word in nltk.word_tokenize(sentence) if any(c.isalpha() for c in word)]) 
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunk = list()
    for sub in tree.subtrees(lambda s: s.height()!=tree.height()):
        if any(sub_sub.label() == "NP" for sub_sub in sub.subtrees(lambda s:s.height()!= sub.height())):
                continue
        elif sub.label() == "NP":
            chunk.append(sub)
    return chunk

# subtrees include the tree itself



if __name__ == "__main__":
    main()
