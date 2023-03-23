import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            #  (person in have_trait) is a bool
            for person in names
        )
        if fails_evidence:
            continue
        # continue means do the next loop

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]
# itertools.chain.from_iterable() flatten out iterable
# itertools.combinations(s,r) return a tuple, which includes all the possible combinations of r elements of s

def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    single_prob = dict()
    names = set(people)
    no_gene = names - one_gene- two_genes
    for no in no_gene:
        if people[no]["mother"] == None and people[no]["father"] == None:
            join = PROBS["gene"][0]
        elif people[no]["mother"] in one_gene and people[no]["father"] in one_gene:
            join = 0.5*0.5*(1-PROBS["mutation"])*(1-PROBS["mutation"])+0.5*0.5*PROBS["mutation"]*(1-PROBS["mutation"])*2+0.5*0.5*PROBS["mutation"]*PROBS["mutation"]
        elif (people[no]["mother"] in one_gene and people[no]["father"] in two_genes) or (people[no]["mother"] in two_genes and people[no]["father"] in one_gene):
            join = 0.5*(1-PROBS["mutation"])*PROBS["mutation"]+0.5*PROBS["mutation"]*PROBS["mutation"]
        elif people[no]["father"] in two_genes and people[no]["mother"] in two_genes:
            join = PROBS["mutation"] * PROBS["mutation"]
        elif people[no]["father"] in no_gene and people[no]["mother"] in no_gene:
            join = (1-PROBS["mutation"]) * (1-PROBS["mutation"])
        elif (people[no]["father"] in no_gene and people[no]["mother"] in one_gene) or (people[no]["mother"] in no_gene and people[no]["father"] in one_gene):
            join = (1-PROBS["mutation"])*(1-PROBS["mutation"])*0.5+(1-PROBS["mutation"])*PROBS["mutation"]*0.5
        else:
            join = (1-PROBS["mutation"])*PROBS["mutation"]
        if no in have_trait:
            single_prob[no] = join *PROBS["trait"][0][True]
        else:
            single_prob[no] = join *PROBS["trait"][0][False]
    
    for one in one_gene:
        if people[one]["mother"] == None and people[one]["father"] == None:
            join = PROBS["gene"][1]
        elif people[one]["mother"] in one_gene and people[one]["father"] in one_gene:
            join = 0.5*0.5*(1-PROBS["mutation"])*(1-PROBS["mutation"])*2+0.5*0.5*PROBS["mutation"]*(1-PROBS["mutation"])*2+0.5*0.5*PROBS["mutation"]*2
        elif (people[one]["mother"] in one_gene and people[one]["father"] in two_genes) or (people[one]["mother"] in two_genes and people[one]["father"] in one_gene):
            join = 0.5*(1-PROBS["mutation"])*(1-PROBS["mutation"])+0.5*PROBS["mutation"]*(1-PROBS["mutation"])+PROBS["mutation"]*0.5*PROBS["mutation"]+0.5*PROBS["mutation"]*(1-PROBS["mutation"])
        elif people[one]["father"] in two_genes and people[one]["mother"] in two_genes:
            join = PROBS["mutation"] * (1-PROBS["mutation"])*2
        elif people[one]["father"] in no_gene and people[one]["mother"] in no_gene:
            join = (1-PROBS["mutation"]) * PROBS["mutation"]*2
        elif (people[one]["father"] in no_gene and people[one]["mother"] in one_gene) or (people[one]["mother"] in no_gene and people[one]["father"] in one_gene):
            join = (1-PROBS["mutation"])*(1-PROBS["mutation"])*0.5+(1-PROBS["mutation"])*PROBS["mutation"]*0.5+PROBS["mutation"]*PROBS["mutation"]*0.5+PROBS["mutation"]*(1-PROBS["mutation"])*0.5
        else:
            join = (1-PROBS["mutation"])*(1-PROBS["mutation"])+PROBS["mutation"]*PROBS["mutation"]
        if one in have_trait:
            single_prob[one] = join *PROBS["trait"][1][True]
        else:
            single_prob[one] = join *PROBS["trait"][1][False]  

    for two in two_genes:
        if people[two]["mother"] == None and people[two]["father"] == None:
            join = PROBS["gene"][2]
        elif people[two]["mother"] in one_gene and people[two]["father"] in one_gene:
            join = 0.5*0.5*(1-PROBS["mutation"])*(1-PROBS["mutation"])+0.5*0.5*PROBS["mutation"]*(1-PROBS["mutation"])*2+0.5*0.5*PROBS["mutation"]
        elif (people[two]["mother"] in one_gene and people[two]["father"] in two_genes) or (people[two]["mother"] in two_genes and people[two]["father"] in one_gene):
            join = 0.5*(1-PROBS["mutation"])*(1-PROBS["mutation"])+0.5*PROBS["mutation"]*(1-PROBS["mutation"])
        elif people[two]["father"] in two_genes and people[two]["mother"] in two_genes:
            join = (1-PROBS["mutation"]) * (1-PROBS["mutation"])
        elif people[two]["father"] in no_gene and people[two]["mother"] in no_gene:
            join = PROBS["mutation"] * PROBS["mutation"]
        elif (people[two]["father"] in no_gene and people[two]["mother"] in one_gene) or (people[two]["mother"] in no_gene and people[two]["father"] in one_gene):
            join = PROBS["mutation"]*(1-PROBS["mutation"])*0.5+PROBS["mutation"]*PROBS["mutation"]*0.5
        else:
            join = (1-PROBS["mutation"])*PROBS["mutation"]
        if two in have_trait:
            single_prob[two] = join *PROBS["trait"][2][True]
        else:
            single_prob[two] = join *PROBS["trait"][2][False]  

    join_prob =1
    for prob in single_prob:
        join_prob = join_prob * single_prob[prob]
    return join_prob

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    names = set(probabilities)
    no_gene = names - one_gene - two_genes
    for person in names:
        if person in no_gene:
            probabilities[person]["gene"][0] += p
        elif person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    sum_trait =0
    sum_gene = 0
    for person in probabilities:
        sum_trait = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        normal_value_trait = 1/sum_trait
        probabilities[person]["trait"][True]=probabilities[person]["trait"][True] * normal_value_trait
        probabilities[person]["trait"][False]=probabilities[person]["trait"][False] * normal_value_trait
        sum_gene = probabilities[person]["gene"][0] + probabilities[person]["gene"][1]+probabilities[person]["gene"][2]
        normal_value_gene = 1/sum_gene
        probabilities[person]["gene"][0] = probabilities[person]["gene"][0]*normal_value_gene
        probabilities[person]["gene"][1] = probabilities[person]["gene"][1]*normal_value_gene
        probabilities[person]["gene"][2] = probabilities[person]["gene"][2]*normal_value_gene


if __name__ == "__main__":
    main()
