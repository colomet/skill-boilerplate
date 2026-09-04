## Trigger evaluation

Optional, on demand. Run it when a skill doesn't load when it should, when the
wrong one loads, or when adding a skill to ground another already covers.

**How triggering actually works:** the `description` is the only input. The body
is not read until after the decision. And skills are consulted for tasks the
model can't already handle in one step — so a trivial test query proves nothing,
because a failure can't be told apart from a task that needed no skill at all.

1. **Map the neighbours.** List the skills sharing vocabulary with this one. For
   each, write the boundary in one sentence. The expensive failure isn't "didn't
   fire" — it's "the neighbour fired".
2. **Write 20 queries**, 10 that should trigger and 10 that shouldn't, in the
   words a real user would type: lowercase, abbreviations, typos, some context,
   varied length. The valuable negatives are near-misses that share vocabulary
   but need something else. An obvious negative proves nothing.
3. **Run each in a fresh conversation**, pasted as-is. Never add "use skill X" —
   that invalidates the test. Repeat borderline ones two or three times;
   triggering is not deterministic.
4. **Read the result:**

| Observed | Diagnosis | Fix |
|---|---|---|
| Positive didn't fire, query was complex | Missing lexical trigger | Add that literal phrasing to the description |
| Positive didn't fire, query was simple | Not a description problem | Change nothing |
| Negative fired | Description too broad | Add the explicit exclusion, naming the right skill |
| The neighbour fired instead | Boundary not declared | Write the boundary in **both** descriptions |
| Nothing ever fires | Description too abstract | Rewrite starting from the concrete thing it produces |

One change per iteration. Two at once and you won't know which worked. A
boundary written in only one of the two descriptions doesn't hold — the other
skill keeps stealing the queries.
