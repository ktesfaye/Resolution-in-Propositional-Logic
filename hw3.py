"""
Kirubel Tesfaye
Project 3
Logic Resolution

In this assignment I implemented inference in propositional logic using resolution.
This program should take KB in a file containing one sentence on each line.
The code expects the knowledge base to conform to the following guidelines:
● The KB has one sentence per line. The last line may optionally start with "goal: "
   and then be followed by the goal sentence.
● Each logical operator consists of a single character:
    ○ not: -
    ○ Conjunction/and: ^
    ○ Disjunction/or: v
    ○ implication: >
    ○ iff: =

"""

import sys

## Classes used for parsing and storing logic.
## You will likely need to change/add to some or all of these, and are not at all
## obligated to use them if you would prefer to store your KB some other way!

class Literal:
    """A propositional logic literal.
    symbol should be a capital letter.
    positive should be a boolean telling whether the literal is positive or not."""

    def __init__(self, symbol, positive, type = "Literal"):
        self.symbol = symbol
        self.positive = positive
        self.type = "Literal"

    def __str__(self):
        if self.positive:
            return self.symbol
        return "-" + self.symbol

    def __repr__(self):
        return str(self)


class Clause:
    """Represents a clause in conjunctive normal form.
    self.literals is a set of Literals in the clause."""

    def __init__(self, literals):
        #SITE:https://stackoverflow.com/questions/6310867/why-arent-python-sets-hashable
        #How to hash a set
        """Literals should be a list or set of Literals."""
        # Since sets are mutable objects, they can't be hashed. But the forzen
        # version a set is mutable, so change the set to frozen.
        self.literals = frozenset(literals)

    def __str__(self):
        if len(self.literals) == 0:
            return "()"

        literal_list = list(self.literals)
        result = "(" + str(literal_list[0])
        for lit in literal_list[1:]:
            result += "v" + str(lit)

        return result + ")"

    def union(self, other):
        """Unions two Clauses, and returns a new Clause"""
        new_literals = self.literals | other.literals
        return Clause(new_literals)


class Negate:
    """ Returns a negated version of the premise """
    def __init__(self, symbol, type = None):
        # Take a premise, could be literal, conjunction, or disjunction
        self.symbol = symbol

        # Keep track of the original positivity of the premise
        self.temp_positive = self.symbol.positive

        # After it gets negated, its positive value would be false
        self.positive = False

        self.type = symbol.type

        # The object of this class is Negate, so if you want to access the args
        # of the premise, you can use arg1 or arg2.
        if self.symbol.type != "Literal":
            self.arg1 = self.symbol.arg1
            self.arg2 = self.symbol.arg2


    def __str__(self):
        # Negate the given premise and return it with the correct syntax.
        #-----------------Handle double negations-------------------------------
        if not self.temp_positive:
            if self.symbol.type == "Literal":
                return self.symbol.symbol

            elif self.symbol.type == "Disjunction":
                return "({}v{})".format(self.symbol.arg1, self.symbol.arg2)

            elif self.symbol.type == "Conjunction":
                return "({}^{})".format(self.symbol.arg1, self.symbol.arg2)

        #-----------------------------------------------------------------------

        #-------------Distributive property of negation-------------------------
        if self.symbol.type == "Disjunction":
            # By default, just negate the args and put them in conjunction form
            arg1 = "{}{}".format("-", self.symbol.arg1)
            arg2 = "{}{}".format("-", self.symbol.arg2)

            # Handle double negation of the args
            if self.symbol.arg1.positive == False:
                arg1 = "{}".format(self.symbol.arg1.symbol)
            if self.symbol.arg2.positive == False:
                arg2 = "{}".format(self.symbol.arg2.symbol)

            # return the correct formated negated version
            return "({}^{})".format(arg1, arg2)

        if self.symbol.type == "Conjunction":
            # By default, just negate the args and put them in disjunction form
            arg1 = "{}{}".format("-", self.symbol.arg1)
            arg2 = "{}{}".format("-", self.symbol.arg2)

            # Handle double negation of the args
            if self.symbol.arg1.positive == False:
                arg1 = "{}".format(self.symbol.arg1.symbol)
            if self.symbol.arg2.positive == False:
                arg2 = "{}".format(self.symbol.arg2.symbol)

            # return the correct formated negated version
            return "({}v{})".format(arg1, arg2)
            # return "({}{}v{}{})".format("-", self.symbol.arg1, "-", self.symbol.arg2)

        #-----------------------------------------------------------------------

        #-------------------Negate Literals------------------------------------

        # At this point, just return the negated version since no double negations
        # would reach this level

        string = ""
        string += "-"

        # return the correct formated negated version
        string += "{}".format(self.symbol)

        return string

    def __repr__(self):
        return str(self)


class Disjunction:
    """Class for a disjunction (or)."""

    def __init__(self, arg1, arg2, positive, type = "Disjunction"):
        self.arg1 = arg1
        self.arg2 = arg2
        self.positive = positive
        self.type = "Disjunction"

    def __str__(self):
        string = ""
        if not self.positive:
            string += "-"

        string += "({}v{})".format(self.arg1, self.arg2)
        return string

    def __repr__(self):
        return str(self)


class Conjunction:
    """Class for a conjunction (and)."""

    def __init__(self, arg1, arg2, positive, type = "Conjunction"):
        self.arg1 = arg1
        self.arg2 = arg2
        self.positive = positive
        self.type = "Conjunction"

    def __str__(self):
        string = ""
        if not self.positive:
            string += "-"

        string += "({}^{})".format(self.arg1, self.arg2)
        return string

    def __repr__(self):
        return str(self)


class Implication:
    """Class for an implication."""

    def __init__(self, arg1, arg2, positive, type = "Implication"):
        self.arg1 = arg1
        self.arg2 = arg2
        self.positive = positive
        self.type = "Implication"

    def __str__(self):
        string = ""
        if not self.positive:
            string += "-"

        string += "({}>{})".format(self.arg1, self.arg2)
        return string

    def __repr__(self):
        return str(self)


class IfAndOnlyIf:
    """Class for If And Only If."""

    def __init__(self, arg1, arg2, positive, type = "IfAndOnlyIf"):
        self.arg1 = arg1
        self.arg2 = arg2
        self.positive = positive
        self.type = "IfAndOnlyIf"

    def __str__(self):
        string = ""
        if not self.positive:
            string += "-"

        string += "({}={})".format(self.arg1, self.arg2)
        return string

    def __repr__(self):
        return str(self)


################################ PARSING #######################################
def distribute_ors(word):
    if word.type != "Literal":
        # Demograns Law
        # Convert sentences in the form of (a^b)v(c^d)->(avc)^(bvc)^(avd)^(bvd)
        if word.type == "Disjunction" and word.arg1.type == "Conjunction" and word.arg2.type == "Conjunction":
                part1 = Disjunction(word.arg1, word.arg2.arg1, True)
                part2 = Disjunction(word.arg1, word.arg2 .arg2, True)
                word = Conjunction(part1, part2, True)

                part1 = Disjunction(word.arg1.arg1.arg1, word.arg1.arg2, True)
                part2 = Disjunction(word.arg1.arg1.arg2, word.arg1.arg2, True)
                word.arg1 = Conjunction(part1, part2, True)

                part1 = Disjunction(word.arg2.arg1.arg1, word.arg2.arg2, True)
                part2 = Disjunction(word.arg2.arg1.arg2, word.arg2.arg2, True)
                word.arg2 = Conjunction(part1, part2, True)

        # Convert sentences in the form of av(b^c)->(avb)^(avc)
        elif word.type == "Disjunction" and word.arg2.type == "Conjunction":
            part1 = Disjunction(word.arg1, word.arg2.arg1, True)
            part2 = Disjunction(word.arg1, word.arg2.arg2, True)
            word = Conjunction(part1, part2, True)

        # Convert sentences in the form of (a^b)vc-> (avc)^(bvc)
        elif word.type == "Disjunction" and word.arg1.type == "Conjunction":
            part1 = Disjunction(word.arg1.arg1, word.arg2, True)
            part2 = Disjunction(word.arg1.arg2, word.arg2, True)
            word = Conjunction(part1, part2, True)

        return word
    return word

def set_of_clauses_generator(word):
    """ Take a clause and return a set of all the literals and conjunctions """
    # First, distribute any ors you find to its proper form
    word = distribute_ors(word)

    # If you reach to the literal, just return it in the set
    if word.type == "Literal":
        arg1clause = Clause([word])
    elif word.arg1.type == "Literal":
        arg1clause = Clause([word.arg1])
    elif word.type == "Conjunction":
        if word.arg1.arg1.type == "Literal" and word.arg1.arg2.type == "Literal":
            arg1clause = Clause([word.arg1])
        else:
            arg1clause = set_of_clauses_generator(word.arg1)
    elif word.type == "Disjunction":
        arg1clause = set_of_clauses_generator(word.arg1)
    # If it is a disjunction, break it up into literals
    elif word.arg1.type == "Disjunction":
        arg1clause = set_of_clauses_generator(word.arg1)
    # If it is conjunction, return it as its own clause
    elif word.arg1.type == "Conjunction":
        arg1clause = set_of_clauses_generator(word.arg1)
    else:
        raise Exception("Something went wrong here! Arg1")

        # If you reach to the literal, just return it in the set
    if word.type == "Literal":
        arg2clause = Clause([word])
    elif word.arg2.type == "Literal":
        arg2clause = Clause([word.arg2])
    elif word.type == "Conjunction":
        if word.arg2.arg1.type == "Literal" and word.arg2.arg2.type == "Literal":
            arg2clause = Clause([word.arg2])
        else:
            arg2clause = set_of_clauses_generator(word.arg2)
    elif word.type == "Disjunction":
        arg2clause = set_of_clauses_generator(word.arg2)
    # If it is a disjunction, break it up into literals
    elif word.arg2.type == "Disjunction":
        arg2clause = set_of_clauses_generator(word.arg2)
    # If it is conjunction, return it as its own clause
    elif word.arg2.type == "Conjunction":
        arg2clause = set_of_clauses_generator(word.arg2)
    else:
        raise Exception("Something went wrong here! Arg2")

    return arg1clause.union(arg2clause)

def tokenize_sentence(sentence):
    """Tokenizes a sentence."""

    tokens = []
    positive = True
    parentheses = 0
    current_parenthesized_token = ""

    for char in sentence:
        if char == "(":
            # Start or continue a parenthesis block
            parentheses += 1
            current_parenthesized_token += "("
        elif char == ")":
            # A matching parenthesis!
            parentheses -= 1
            current_parenthesized_token += ")"
            if parentheses == 0:
                # We've finished a parenthesized block
                if not positive:
                    current_parenthesized_token = "-" + current_parenthesized_token
                tokens.append(current_parenthesized_token)
                current_parenthesized_token = ""
                positive = True

        elif parentheses > 0:
            # In a parenthesis block; just add the char to the token
            current_parenthesized_token += char

        else:
            # Not in a parenthesis block

            if char == "-":
                # Negate whatever's next
                positive = not positive

            elif char in "v^>=":
                # Add the character to tokens if it is a binary logical operator
                tokens.append(char)

            else:
                # Handle literals by making a Literal object
                lit = Literal(char, positive)
                tokens.append(lit)
                positive = True

    return tokens

def unwrap_parens_if_necessary(token):
    """If token is a parenthesized block, unwraps it and returns it."""
    if not isinstance(token, str):
        return token

    if token[0] == "-":
        token = token[1:]

    if token[0] == "(":
        return token[1:-1]

    print("You PROBABLY should never get here. Token =", token)

    return token

def turn_tokens_into_objects(tokens):
    """Turns a list of 3+ tokens into objects. And convert to CNF"""

    argument1 = parse_sentence(unwrap_parens_if_necessary(tokens[0]))
    if isinstance(tokens[0], str) and tokens[0][0] == "-":
        argument1.positive = False

        # Distribute the negative to make later manipulation easier
        if argument1.type == "Disjunction":
            argument1 = Conjunction(Negate(argument1.arg1), Negate(argument1.arg2), True)

        elif argument1.type == "Conjunction":
            argument1 = Disjunction(Negate(argument1.arg1), Negate(argument1.arg2), True)

    if len(tokens) == 3:
        argument2 = parse_sentence(unwrap_parens_if_necessary(tokens[2]))
        if isinstance(tokens[2], str) and tokens[2][0] == "-":
            argument2.positive = False

            # Distribute the negative to make later manipulation easier
            if argument2.type == "Disjunction":
                argument2 = Conjunction(Negate(argument2.arg1), Negate(argument2.arg2), True)

            elif argument2.type == "Conjunction":
                argument2 = Disjunction(Negate(argument2.arg1), Negate(argument2.arg2), True)

    else:
        # Recursively turn tokens into objects
        argument2 = turn_tokens_into_objects(tokens[2:])

    first_operator = tokens[1]

    # ------------------Convert Input to CNF------------------------------------
    if first_operator == "=":
        # If you encounter an iff, convert it to the form of
        # (a = b) -> (a > b) ^ (b > a)
        part1 = Implication(argument1, argument2, True)
        part2 = Implication(argument2, argument1, True)
        iff = Conjunction(part1, part2, True)

        # Now, convert the implication to the form of
        # (a > b) -> (-a v b)
        if iff.arg1.type == "Implication":
            iff.arg1 = Disjunction(Negate(iff.arg1.arg1), iff.arg1.arg2, True)

        if iff.arg2.type == "Implication":
            iff.arg2 = Disjunction(Negate(iff.arg2.arg1), iff.arg2.arg2, True)

        # At this point, the iff is converted to its CNF counterpart
        return iff

    elif first_operator == ">":
        # If you encounter an implication, convert it to the form of
        # (a > b) -> (-a v b)
        return Disjunction(Negate(argument1), argument2, True)
    elif first_operator == "v":
        return Disjunction(argument1, argument2, True)
    elif first_operator == "^":
        return Conjunction(argument1, argument2, True)

    raise SyntaxError("Unrecognized argument.")

def parse_sentence(sentence_string):
    """Parses a sentence string into a sentence, which is one of these types
    of objects:
        - Literal
        - Conjunction (and)
        - Disjunction (or)
        - Implication
        - IfAndOnlyIf
    """

    # If sentence_string is not a string, it has already been parsed. Return it.
    if not isinstance(sentence_string, str):
        return sentence_string

    tokens = tokenize_sentence(sentence_string)

    # Handle single literal tokens
    if len(tokens) == 1:
        return tokens[0]

    first_operator = tokens[1]

    # Make sure exactly 3 tokens if first operator is > or =
    if first_operator in ">=":
        assert len(tokens) == 3

    # Make sure all operators are the same if there are more than one and they are ^ or v
    for odd_index in range(1, len(tokens), 2):
        assert tokens[odd_index] == first_operator

    # Now, we can turn tokens into the right things recursively
    return turn_tokens_into_objects(tokens)

def parse_input():
    """Returns list of sentences in KB and goal sentence if present.
    Sentences and goal are parsed into objects representing each sentence,
    though they have not been transformed into equivalent conjunctive-normal form."""

    sentences = []
    goal = None

    for line in sys.stdin:
        line = line.strip()
        print("ORIGINAL: ", line)
        # Detect the goal line separately
        if line.startswith("goal: "):
            goal = parse_sentence(line[len("goal: "):])
        else:
            sentence = parse_sentence(line)
            sentences.append(sentence)

    return sentences, goal

def res_helper(literal, sentences, dictionary):
    """ For resultion, take a literal and iterate it through the whole
    KB and find its complimentary literal. """


    for clauses in list(dictionary):
        # For each line in the KB, convert it to a set of literals

        # Once  clause is complitely resolved, don't visit it
        if clauses == frozenset():
            dictionary[clauses] = True

        # Since a frozen set is not mutable, convert it to a normal set
        clauses = set(clauses)

        # Grab a second literal to test if its complimentary to the og lit
        for sec_literal in clauses:
            # As long as the current clause is not one thats already resolved, use it
            if dictionary[frozenset(clauses)] == False:

                # Literals are complimentary, if their symbol is the same
                # and their positivity is opposite
                if sec_literal.type == "Disjunction" and literal.type == "Disjunction":
                    if (literal.arg1.symbol == sec_literal.arg1.symbol and literal.arg1.positive != sec_literal.arg1.positive) and (literal.arg2.symbol == sec_literal.arg2.symbol and literal.arg2.positive != sec_literal.arg2.positive):
                        # Once a clause is found, mark that it is resolved
                        dictionary.update({frozenset(clauses):True})

                        # Resolve the literals
                        clauses.remove(sec_literal)

                        # Add a new clause
                        dictionary[frozenset(clauses)] = False

                        # Return the resolved clause
                        return True
                elif sec_literal.type == "Disjunction" or literal.type == "Disjunction" or sec_literal.type == "Conjunction" or literal.type == "Conjunction":
                    pass
                elif literal.symbol == sec_literal.symbol and literal.positive != sec_literal.positive:
                    # Once a clause is found, mark that it is resolved
                    dictionary.update({frozenset(clauses):True})

                    # Resolve the literals
                    clauses.remove(sec_literal)

                    # Add a new clause
                    dictionary[frozenset(clauses)] = False

                    # Return the resolved clause
                    return True

def recure(sentences, dictionary):
    """ Another helper for the resolution fun. Pick the first literal and
    find its complimentary """

    # Run this function about 1000, and if by then a solution is not found,
    # then you know the KB is not entailed
    for _ in range(1000):
        # Exactly the same format as the fun above, except this one grabs the
        # first literal, and the other fun finds its opposite.

        for key_word in list(dictionary):
            key_word = set(key_word)

            if key_word == frozenset():
                dictionary[frozenset(key_word)] = True

            if dictionary[frozenset(key_word)] == False:
                for literal in key_word:
                    result = res_helper(literal, sentences, dictionary)
                    if result == True:
                        dictionary.update({frozenset(key_word):True})

                        key_word.remove(literal)

                        dictionary[frozenset(key_word)] = False
                        break

        # SITE: https://stackoverflow.com/questions/10666163/how-to-check-if-all-elements-of-a-list-matches-a-condition
        # DESC: If all the values are true, that means all the clauses are resolved
        #       in which case you are set!
        if all(flag == True for (flag) in dictionary.values()):
            print("Whoray!! The KB enatails the sentence! :)")
            return dictionary

    # If it gets here, that means the KB is not resolved :(
    print("Boo! The KB does not entail the sentence :(")

def resolution():
    """ Resolve the KB """

    # Input the KB
    sentences, goal = parse_input()

    # A dict to mark clause status
    dictionary = {}

    if goal != None:
        sentences.append(distribute_ors(Negate(goal)))
    print()
    for word in sentences:
        print("CNF: ", word)

    # Fill the dictionary with the KB and set their values to Flase.
    for word in range(len(sentences)):
        set_of_clauses = set_of_clauses_generator(sentences[word]).literals
        dictionary[set_of_clauses] = False

    # print(dictionary)
    print()
    recure(sentences, dictionary)
    # print()
    # print(dictionary)

################################################################################
## You will need to add to the main function to actually store the KB
## and use it in resolution.

def main():

    # Resolve
    resolution()


if __name__ == "__main__":
    main()
