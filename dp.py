import argparse
import time

def parsing(file_path):
    clauses = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(('c', '%')):
                continue
            if line.startswith('p'):
                continue
            parts = [p for p in line.split() if p not in ('', '0')]
            if parts:
                clauses.append(set(int(lit) for lit in parts))
    return clauses

def propagate(clauses):
    assignments = {}
    changed = True
    while changed:
        changed = False
        units = [next(iter(c)) for c in clauses if len(c) == 1]
        for lit in units:
            var = abs(lit)
            val = lit > 0
            if var in assignments and assignments[var] != val:
                return clauses, True
            assignments[var] = val
            changed = True
            clauses = [c - {-lit} for c in clauses if lit not in c]
            break
    return clauses, False

def pure(clauses):
    counts = {}
    for c in clauses:
        for lit in c:
            counts[lit] = counts.get(lit, 0) + 1
    pure_lits = [lit for lit in counts if -lit not in counts]
    if not pure_lits:
        return clauses, False
    return [c for c in clauses if not any(l in c for l in pure_lits)], True

def solve(clauses, stats):
    stats['calls'] += 1
    clauses, conflict = propagate(clauses)
    if conflict:
        return False 
    clauses, changed = pure(clauses)
    if changed:
        return solve(clauses, stats)
    if not clauses:
        return True
    if any(not c for c in clauses):
        return False
    for c in clauses:
        for lit in c:
            if -lit in {l for clause in clauses for l in clause}:
                var = lit
                break
        break
    pos = [c for c in clauses if var in c]
    neg = [c for c in clauses if -var in c]
    resolvents = []
    for c in pos:
        for d in neg:
            resolvent = (c - {var}).union(d - {-var})
            if any(lit in resolvent and -lit in resolvent for lit in resolvent):
                continue
            resolvents.append(resolvent)
    remaining = [c for c in clauses if var not in c and -var not in c]
    return solve(remaining + resolvents, stats)

def main():
    parser = argparse.ArgumentParser(description="DP SAT Solver")
    parser.add_argument("-i", "--input", required=True, help="Input CNF file")
    args = parser.parse_args()

    start = time.time()

    clauses = parsing(args.input)
    stats = {'calls': 0}
    result = solve(clauses, stats)

    end = time.time()

    print("SAT!" if result else "UNSAT!")
    print(f"Recursive calls: {stats['calls']}")
    print(f"Time: {end - start:.4f}s")

if __name__ == "__main__":
    main()