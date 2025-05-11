# SATSolvers
The 3 SAT Solving algorithms (Resolution, DP and DPLL) from the "Comparative Analysis of SAT Solvers: Resolution, Davis-Putnam, and DPLL"
User Manual
1. Requirements
– Python 3
2. Usage: In the terminal, write:
python [resolution.py/dp.py/dpll.py] -i "<path to the .cnf file>"
3. Input format: .cnf files should follow the DIMACS CNF format (should
look like this:)
p cnf 3 3
1 2 0
-1 2 0
-2 -3 0
– p cnf 3 3 tells the program there’s 3 variables and 3 clauses.
– 1 2 0 lines representing clauses, the 0 at the end shows the end of the
clause.
