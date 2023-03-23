import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                    # if letters[i][j] is not None, print letters[i][j], else print " "
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.crossword.variables:
            var_len = var.length
            for word in self.crossword.words:
                if len(word) != var_len:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps[x, y]
        revised = False
        if overlap != None:
            i = overlap[0]
            j = overlap[1]
            # first create a bool to record whether revised or not, return the bool in the end
            values = self.domains[x].copy()
            for value_x in values:
                count = 0
                for value_y in self.domains[y]:
                    if value_x[i] != value_y[j]:
                        count +=1
                if count == len(self.domains[y]):
                    self.domains[x].remove(value_x)
                    revised = True
        return revised


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = set()
            for x in self.crossword.variables:
                for y in self.crossword.variables:
                    if x == y:
                        continue
                    else:
                        if self.crossword.overlaps[x,y] !=None:
                            arcs.add((x,y))
        while len(arcs)>0:
            arc = arcs.pop()
            x = arc[0]
            y = arc[1]
            if self.revise(x, y):
                if self.domains[x] is None:
                    return False
                for neighbor in self.crossword.neighbors(x):
                    arcs.add((neighbor,x))
        return True
        

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(self.crossword.variables):
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for var in assignment:
            value = assignment[var]
            if len(value) != var.length:
                return False
            for var2 in assignment:
                if var == var2:
                    continue
                if assignment[var] == assignment[var2]:
                    return False
            for z in self.crossword.neighbors(var):
                if z in assignment:
                    i, j = self.crossword.overlaps[var,z]
                    if value[i] != assignment[z][j]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        unordered = list()
        values = self.domains[var]
        variables = self.crossword.variables
        for value in values:
            count = 0
            for z in variables:
                if not z in assignment and z in self.crossword.neighbors(var):
                    i, j = self.crossword.overlaps[var,z]
                    for z_value in self.domains[z]:
                        if value[i]!=z_value[j]:
                            count +=1
            unordered.append({"value":value, "number reduced": count})
        sorted_list = sorted(unordered, key = lambda s:s["number reduced"])
        ordered = list()
        for value in sorted_list:
            ordered.append(value["value"])
        return ordered
    
        

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_variables = list()
        assigned = set(assignment)
        for var in self.crossword.variables:
            if var not in assigned:
                unassigned_variables.append({"variable":var, "number":len(self.domains[var])})
        sorted_list = sorted(unassigned_variables, key = lambda s:(s["number"], -len(self.crossword.neighbors(s["variable"]))))
        # sort by two keys, one reversed
        return sorted_list[0]["variable"]
        


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        values = self.order_domain_values(var, assignment)
        for value in values:
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
                # if the recurssive function returns None, it needs try another value
                # when reaching the end of the recursive function, always check where you call the function
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
