
import argparse
import time

def parsing(file_path):
    clauses = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line[0] in ['c', '%']:
                continue
            if line.startswith('p'):
                continue
            parts = line.split()
            clause = set()
            for lit in parts:
                if lit == '' or lit == '0':
                    continue
                clause.add(int(lit))
            if clause:
                clauses.append(clause)
    return clauses

def propagate(clauses):
    assignments = {}
    changed = True
    while changed:
        changed = False
        units = []
        for c in clauses:
            if len(c) == 1:
                units.append(next(iter(c)))
        for lit in units:
            var = abs(lit)
            val = lit > 0
            if var in assignments:
                if assignments[var] != val:
                    return clauses, True
            assignments[var] = val
            changed = True
            new_clauses = []
            for c in clauses:
                if lit in c:
                    continue
                new_c = set()
                has_neg_lit = False
                for l in c:
                    if l == -lit:
                        has_neg_lit = True
                    else:
                        new_c.add(l)
                if has_neg_lit:
                    if not new_c:
                        return [new_c], True
                    new_clauses.append(new_c)
                else:
                    new_clauses.append(set(c))
            clauses = new_clauses
            break
    return clauses, False

def pure(clauses):
    lit_counts = {}
    for c in clauses:
        for lit in c:
            if lit in lit_counts:
                lit_counts[lit] += 1
            else:
                lit_counts[lit] = 1
    pure_lits = []
    for lit in lit_counts:
        if -lit not in lit_counts:
            pure_lits.append(lit)
    if not pure_lits:
        return clauses, False
    new_clauses = []
    for c in clauses:
        keep = True
        for l in pure_lits:
            if l in c:
                keep = False
                break
        if keep:
            new_clauses.append(set(c))
    return new_clauses, True

def simplify(clauses, lit):
    new_clauses = []
    for c in clauses:
        if lit in c:
            continue
        new_c = set()
        for l in c:
            if l != -lit:
                new_c.add(l)
        new_clauses.append(new_c)
    return new_clauses

def dpll(clauses, stats):
    stats['calls'] += 1
    
    clauses, conflict = propagate(clauses)
    if conflict:
        return False
        
    clauses, changed = pure(clauses)
    if changed:
        return dpll(clauses, stats)
    
    if not clauses:
        return True
    empty_clause = False
    for c in clauses:
        if not c:
            empty_clause = True
            break
    if empty_clause:
        return False
        
    lit = None
    for l in clauses[0]:
        lit = l
        break
    
    if dpll(simplify(clauses, lit), stats):
        return True
    return dpll(simplify(clauses, -lit), stats)

def main():
    parser = argparse.ArgumentParser(description="DPLL SAT Solver")
    parser.add_argument("-i", "--input", required=True, help="Input CNF file")
    args = parser.parse_args()

    start_time = time.time()

    clauses = parsing(args.input)
    stats = {'calls': 0}
    result = dpll(clauses, stats)

    end_time = time.time()

    print("SAT!" if result else "UNSAT!")
    print(f"Recursive calls: {stats['calls']}")
    print(f"Time elapsed: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()