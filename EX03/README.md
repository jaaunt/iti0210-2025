# EX03 - Forward Chaining Assignment

## 1. Knowledge Base

The program accepts the following **knowledge base** as input:

- 6
- Egg is fragile
- Egg falls down
- Egg contains liquid
- Egg is fragile & Egg falls down -> Egg breaks
- Egg breaks & Egg contains liquid -> Egg makes a mess
- Egg is spoiled & Egg breaks -> Egg smells
- Egg breaks


- Lines without `->` are considered **facts**.  
- Lines with `->` are considered **implications/rules**.

---

## 2. Queries and Results

The program produces the following results for the queries:

| Query             | Result |
|------------------|--------|
| Egg breaks        | YES    |
| Egg makes a mess  | YES    |
| Egg smells        | NO     |

---

## 3. Step-by-Step Reasoning for Query: "Egg makes a mess"

We want to determine whether `"Egg makes a mess"` can be derived using the **forward chaining algorithm**.

### Step 1 - Initialize known facts

- Agenda (facts to process): ["Egg is fragile", "Egg falls down", "Egg contains liquid"]
- Proven facts (already known): {"Egg is fragile", "Egg falls down", "Egg contains liquid"}


- `parse_clause` splits input into (premises, conclusion) pairs.  
- Lines without `->` have empty premises → these are added to `agenda` and `proven_facts`.

---

### Step 2 - Process facts in agenda

1. **Fact: "Egg is fragile"**
   - Check rules that use this as a premise:
     - `"Egg is fragile & Egg falls down -> Egg breaks"` -> 1 premise satisfied (still needs "Egg falls down")  

2. **Fact: "Egg falls down"**
   - Check rules:
     - `"Egg is fragile & Egg falls down -> Egg breaks"` -> all premises satisfied -> **derive "Egg breaks"**  
     - Add `"Egg breaks"` to `agenda` and `proven_facts`  

3. **Fact: "Egg contains liquid"**
   - Check rules:
     - `"Egg breaks & Egg contains liquid -> Egg makes a mess"` -> 1 premise satisfied (still needs "Egg breaks")  

---

### Step 3 - Process newly derived facts

1. **Fact: "Egg breaks"** (derived in Step 2)  
   - Check rules:
     - `"Egg breaks & Egg contains liquid -> Egg makes a mess"` -> all premises satisfied -> **derive "Egg makes a mess"**  
     - Add `"Egg makes a mess"` to `agenda` and `proven_facts`  

---

### Step 4 - Check query

- `"Egg makes a mess"` is now in `proven_facts`.  
-  When all of the agenda is checked algorithm returns yes since `"Egg makes a mess"` is now in `proven_facts`.
---

## 4. Data Structures Used

| Variable         | Role                                                                             |
|-----------------|----------------------------------------------------------------------------------|
| `proven_facts`  | Set of all facts known to be true (avoids duplicates of the same facts, fast lookup) |
| `agenda`        | deque of facts that need to be processed in the Forward Chaining loop            |
| `implications`  | List of implications/rules in the form (premises, conclusion)                    |
| `count`         | Dictionary tracking how many premises are still unmet for each rule              |

---

## 5. Core Algorithm Overview

1. **Separate facts and rules**:
   - Facts: no premises -> add to `agenda` and `proven_facts`  
   - Implications/Rules: `(premises, conclusion)` -> add to `implications` and track remaining premises that arent checked yet in `count`  

2. **Forward Chaining Loop** (`while agenda`):
   - Pop a fact from the `agenda` que using `popleft()`  
   - For each implication/rule where this fact is a premise:
     - Decrease `count` for that implication/rule  
     - If all premises satisfied -> add conclusion to `proven_facts` and `agenda`   

3. **Termination**:
   - If the loop finishes without deriving the query -> return `"NO"`  otherwise return `"YES"`.

---

## 6. Defence Video

Link:  

