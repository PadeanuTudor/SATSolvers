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
                clause = frozenset(int(lit) for lit in parts)
                if not any(-lit in clause for lit in clause):
                    clauses.append(clause)
    return set(clauses)

def resolve(c1, c2):
    resolvents = set()
    for lit in c1:
        if -lit in c2:
            res = (c1 - {lit}) | (c2 - {-lit})
            if not any(x in res and -x in res for x in res):
                resolvents.add(frozenset(res))
    return resolvents

def solve(clauses, stats):
    closure = set(clauses)
    stats['steps'] = 0
    while True:
        new = set()
        existing = list(closure)
        for i in range(len(existing)):
            for j in range(i+1, len(existing)):
                resolvents = resolve(existing[i], existing[j])
                for r in resolvents:
                    if r not in closure and r not in new:
                        new.add(r)
                        stats['steps'] += 1
                        if not r:
                            return False, stats['steps']
        if not new:
            return True, stats['steps']
        closure.update(new)

def main():
    parser = argparse.ArgumentParser(description="Resolution SAT Solver")
    parser.add_argument("-i", "--input", required=True, help="Input CNF file")
    args = parser.parse_args()

    start = time.time()

    clauses = parsing(args.input)
    stats = {'steps': 0}
    sat, steps = solve(clauses, stats)

    end = time.time()

    print("SAT!" if sat else "UNSAT!")
    print(f"Resolution steps: {steps}")
    print(f"Time: {end - start:.4f}s")

if __name__ == "__main__":
    main()