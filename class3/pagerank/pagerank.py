import os
import random
import re
import sys
from collections import Counter

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
    #  get the list of all files and directories in the specified directory
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    total = len(corpus)
    prob = dict()
    num = len(corpus[page])
    if num ==0:
        for p in corpus:
            prob[p]= 1/total
   
    else:
        for p in corpus:
            if p in corpus[page]:
                prob[p] = damping_factor/num + (1-damping_factor)/total
            else:
                prob[p] = (1-damping_factor)/total
    return prob


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    keys = list()
    for key in corpus:
        keys.append(key)
    sample = random.choice(keys)
    results = list()
    results.append(sample)
    for i in range(n-1):
        prob = transition_model(corpus, sample, damping_factor)
        pages = list()
        values = list()
        for page in prob:
            pages.append(page)
            values.append(prob[page])
        sample = random.choices(pages, weights = values, k =1)
        sample = sample[0]
        results.append(sample)
    
    sample_results = Counter(results)
    prob_results = dict()
    for page in sample_results:
        prob_results[page] = sample_results[page]/10000
    return prob_results

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    reverse = dict()
    keys = list()
    for key in corpus:
        keys.append(key)
    for key in corpus:
        if len(corpus[key]) == 0:
            corpus[key] = set(corpus.keys())
    for i in range(len(keys)):
        links = set()
        for j in range(len(keys)):
            if i != j:
                if keys[i] in corpus[keys[j]]:
                    links.add(keys[j])
                reverse[keys[i]] = links
            
    prob = dict()
    for page in corpus:
        prob[page] = 1/len(corpus)

    def update(prob):
        newprob = dict()
        count =0
        for page in corpus:
            # if len(reverse[page]) == 0:
            #     newprob[page] = 1/len(corpus)*(1-damping_factor)
            # else:
            sum = 0
            for link in reverse[page]:
                sum = sum + prob[link]/len(corpus[link])
            newprob[page] = (1-damping_factor)/len(corpus) + damping_factor *sum
            if abs(newprob[page] - prob[page]) >=0.001:
                count +=1
        if count > 0:
            return update(newprob)
        # return whatever you get from update(newprob)!!!!!!!!!!!! otherwise, the function will go count>0 route and return nothing
        else:
            return newprob
    return update(prob)
    # same here, return whatever you get from the function!!!!!!!!!!!!!!

if __name__ == "__main__":
    main()
