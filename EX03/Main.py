def parse_clause(clause_str):
    """
    Parses a clause string into premises and conclusion.
    Example:
        "A & B -> C"   →  (["A", "B"], "C")
        "A"            →  ([], "A")   (fact)
    """
    clause_str = clause_str.strip()

    if "->" in clause_str:
        premises_str, conclusion = clause_str.split("->")
        premises = [p.strip() for p in premises_str.split("&")]
        conclusion = conclusion.strip()
    else:
        # If no '->', this is a fact (no premises)
        premises = []
        conclusion = clause_str

    return (premises, conclusion)


def forward_chaining(clauses, query):
    """
    Forward chaining algorithm for propositional logic inference.
    Determines if 'query' can be derived from the given knowledge base.
    """
    inferred = set()
    agenda = []
    rules = []
    count = {}

    # Step 1: Separate facts and rules
    for premises, conclusion in clauses:
        if not premises:
            # A fact add directly to inferred and agenda
            inferred.add(conclusion)
            agenda.append(conclusion)
        else:
            # A rule store it and initialize its counter
            rules.append((premises, conclusion))
            count[(tuple(premises), conclusion)] = len(premises)

    # Step 2: Forward chaining loop
    while agenda:
        fact = agenda.pop(0)  # take one known fact

        # If weve proven the query, we can stop
        if fact == query:
            return "YES"

        # For every rule that uses this fact as a premise
        for premises, conclusion in rules:
            if fact in premises:
                count[(tuple(premises), conclusion)] -= 1  # one less unknown premise

                # If all premises are now satisfied
                if count[(tuple(premises), conclusion)] == 0:
                    if conclusion not in inferred:
                        inferred.add(conclusion)
                        agenda.append(conclusion)  # new fact discovered

    # Step 3: If we finish and never derived the query
    return "YES" if query in inferred else "NO"


if __name__ == "__main__":
    num_clauses = int(input().strip())
    clauses_raw = [input().strip() for _ in range(num_clauses)]
    query = input().strip()

    clauses = [parse_clause(line) for line in clauses_raw]

    result = forward_chaining(clauses, query)

    print(result)
