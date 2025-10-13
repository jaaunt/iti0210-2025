def parse_clause(clause_str):
    """
    Parses a clause string into premises and conclusion.
    Example:
        "A & B -> C"   →  (["A", "B"], "C")
        "A"            →  ([], "A")   (fact)
    """
    # make input easier to use, lists over strings any day
    clause_str = clause_str.strip()  # remove unneeded spaces

    if "->" in clause_str:  # conclusion has premise(eeldus) and conclusion(jareldus) and -> inbetween
        premises_str, conclusion = clause_str.split("->")  # split the parts
        premises = [p.strip() for p in premises_str.split("&")]
        # split the premise into parts and remove unneeded spaces from both
        conclusion = conclusion.strip()  # remove spaces from the conclusion part
    else:
        # if it doesnt have a -> its a fact
        premises = []  # doesnt have a premise, empty list
        conclusion = clause_str  # whole line is the conclusion

    return (premises, conclusion)  # return both parts


def forward_chaining(clauses, query):
    """
    Forward chaining algorithm for propositional logic inference.
    Determines if 'query' can be derived from the given knowledge base.
    """
    proven_facts = set()  # all proven facts (no dublicates)
    agenda = []  # whats on the agenda aka what hasnt been cheked yet :D, pretty much like a que of unchecked statements
    implications = []  # same shit as before, just conclusions said diffrently...
    count = {}  # how many implications unfulfilled

    # first seperate premises and conclusions in clauses
    for premises, conclusion in clauses:
        if not premises:
            # if there is no premise its a fact add to facts and to the agenda
            proven_facts.add(conclusion)
            agenda.append(conclusion)
        else:
            # its an implication(jareldus)
            implications.append((premises, conclusion))
            count[(tuple(premises), conclusion)] = len(premises)  # add into a dictionary, key example ("A", "B"), "C"
            # where a and b are premises and c is the conclusion and the keys value is the amount of premises that need to be checked

    while agenda:
        fact = agenda.pop(0)  # take one known fact from the agenda (the first and remmove it)

        # split the implication into parts to check separately
        for premises, conclusion in implications:
            if fact in premises:  # if its in the premise
                count[(tuple(premises), conclusion)] -= 1  # remove one from unknown premises

                # if all preises are solved
                if count[(tuple(premises), conclusion)] == 0:
                    if conclusion not in proven_facts:  # since premises were true the conclusion must be true add it to facts
                        proven_facts.add(conclusion)
                        agenda.append(conclusion)

    # check again if the query is in proven facts return yes otherwise no
    return "YES" if query in proven_facts else "NO"


if __name__ == "__main__":
    num_clauses = int(input().strip())
    clauses_raw = [input().strip() for _ in range(num_clauses)]
    query = input().strip()

    clauses = [parse_clause(line) for line in clauses_raw]

    result = forward_chaining(clauses, query)

    print(result)
