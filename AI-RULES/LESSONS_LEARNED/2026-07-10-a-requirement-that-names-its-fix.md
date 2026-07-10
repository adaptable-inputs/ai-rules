---
applies_to:
  load: "never"
  reason: "maintainer lessons-learned record for the ai-rules repository itself"
---
# A requirement that names its fix

A specification stated a property and deliberately declined to name a mechanism. The task text handed to the
implementers put the mechanism back, in a parenthesis. Two implementations then satisfied the mechanism in full and
violated the property. The rule extracted from this is in `CORE/NORMATIVE_LANGUAGE.md`, "State the Observable, Not the
Mechanism".

## What happened

The specification:

> **NFR2 Retrieval cost.** Serving `GET /owners/{id}` MUST NOT perform a separate store lookup per pet or per visit. The
> number of lookups MUST be bounded by a constant, independent of how many pets and visits the owner has. (In an ORM this
> is the N+1 problem; **the requirement is the bound, not the fix**.)

The task text:

> `NFR2: GET /owners/{id} MUST use a bounded number of queries (fetch join or entity graph), never one per pet or per visit.`

The parenthesis converts a property into a checklist, and the checklist is satisfiable while the property fails. Both
named mechanisms fix the associations an author can see -- `o.pets`, `p.visits`. Neither fixes `Pet.type`, which is a
`@ManyToOne` and therefore **EAGER by default** under JPA, so the ORM issues one silent select per pet.

Two implementations walked into it:

- One fetch-joined its queries, reported *"NFR2 served by 3 fixed queries"*, and failed the retrieval-cost test on a
  lazy proxy initialised per traversal. Its own account of its behaviour contradicted the record.
- One shipped an eager `Pet.type` costing 7 statements for 5 pets, then found it -- not by reasoning, but by enabling
  Hibernate statistics and **measuring**. Nothing had asked it to measure. That is the only thing that separated it from
  the first.

## What generalises

- A requirement states an observable. Naming a mechanism turns "did the property hold?" into "did you apply the named
  technique?", and those diverge exactly where the interesting defects live.
- A hint points at the cases its author thought of, and away from the rest. Both suggested fixes address the traversals
  the author writes. Neither addresses the one the mapping adds for free.
- Where a property is measurable, the requirement SHOULD demand the measurement rather than a claim about it. Replacing
  *"MUST use a bounded number of queries (fetch join or entity graph)"* with *"the number of lookups MUST NOT grow with
  the number of pets or visits; measure it at 1 pet and at 4 pets and report both numbers"* leaks nothing, and obliges
  the author to instrument rather than assert.
- An actor's report of its own behaviour is a claim, not a verification -- including when the actor is diligent, and
  including when the claim is true. One implementation's account of its own fix was quoted as a result before the suite
  had confirmed it. It happened to be correct. The suite is what established that.

## Cost of not doing this

One benchmark run failed on a defect the requirement forbade and the task text had inadvertently taught. A second
shipped the same defect and caught it only by instrumenting what it had been told to assume.
