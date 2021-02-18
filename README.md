Your program should read a knowledge base from standard input. I have provided three basic
knowledge bases in CNF, and one knowledge base that is not yet in CNF. You should run your
program as:
python3 hw3.py < kb1.txt
Each knowledge base should be a file containing one sentence on each line. Each sentence will at
minimum be a disjunctive clause (a series of literals separated by "or"), but your program could
support more of propositional logic as well. You may assume that the knowledge base is
correctly formatted; you do not need to gracefully handle errors in the knowledge base.
For the simplest implementations, you can assume that the goal sentence has been negated and
its clauses have been added to the knowledge base. Truly great programs will take the goal
sentence as the last line of the knowledge base, preceded by "goal: ", and will negate it
properly before adding it to the knowledge base.
Your program should use the resolution inference algorithm to determine if the goal can be
inferred by finding a proof by contradiction. Your program should output whether or not the goal
can be inferred from the knowledge base. You may print additional information as you see fit, to
analyze the running of your algorithm.

The KB has one sentence per line. The last line may optionally start with "goal: " and
then be followed by the goal sentence.
● Each logical operator consists of a single character:
○ not: -
○ and: ^
○ or: v
○ implication: >
○ iff: =
● The parser assumes no precedence of operators, so you need to wrap EVERY compound
sentence (composed of more than one logical operator) in parentheses. The only
exceptions to this are:
○ Negation, which should work without parentheses.
○ Chained conjunctions (ands) or disjunctions (ors).
● Here are examples of good and bad inputs:
○ yes: Av-Bv-CvD
○ yes: -A^B^-C^-D
○ no: A=-B=C
○ no: A>B>D
○ no: Av(B^C)vD (though this might work in practice)
○ no: --A (though this might work in practice)
○ no: A^B=C
■ yes: (A^B)=C or A^(B=C)
○ no: C>DvE
■ yes: C>(DvE) or (C>D)vE
