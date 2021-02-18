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
analyze the running of your algorithm
