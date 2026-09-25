# BRIDGE-0001 — DNA four-state algebra to Reality-Code quotient/involution architecture

Status: **FORMALLY PROVED**

Scope: This is a mathematical/formal bridge only. It proves that the canonical four-base DNA alphabet, under a fixed two-bit encoding, carries the same quotient/involution/parity-check structure used by the Reality-Code compiler-invariant framework. It does **not** by itself prove a shared physical substrate, causal mechanism, simulation hypothesis, or biological use of that algebra.

## Fixed encoding

Use the deterministic encoding

- A = (0,0)
- G = (0,1)
- C = (1,0)
- T = (1,1)

Thus the DNA base alphabet is identified with the additive group V = Z2 x Z2 (the Klein four-group).

## Theorem 1 — the three canonical 2+2 base partitions are exactly the three nonzero linear quotients V -> Z2

There are exactly three nonzero linear functionals on V:

1. f_RY(x,y) = x
   - A,G -> 0
   - C,T -> 1
   - therefore this is exactly the purine/pyrimidine partition R/Y.

2. f_MK(x,y) = y
   - A,C -> 0
   - G,T -> 1
   - therefore this is exactly the amino/keto partition M/K.

3. f_WS(x,y) = x XOR y
   - A,T -> 0
   - G,C -> 1
   - therefore this is exactly the weak/strong partition W/S.

Because a two-dimensional vector space over Z2 has exactly three nonzero linear functionals, R/Y, M/K, and W/S exhaust the nontrivial linear one-bit quotients of this encoding. They are not post-hoc members of a larger arbitrary family under this model.

## Theorem 2 — Watson-Crick complement is translation by (1,1)

For each base b with encoding v(b), Watson-Crick complement satisfies

v(comp(b)) = v(b) + (1,1)  (mod 2).

Truth table:

- A (0,0) + (1,1) = T (1,1)
- T (1,1) + (1,1) = A (0,0)
- G (0,1) + (1,1) = C (1,0)
- C (1,0) + (1,1) = G (0,1)

Therefore complement is an involution because applying the same translation twice adds (0,0).

## Theorem 3 — the three canonical quotients form a single-parity-check code

Let

- r = f_RY(x,y)
- m = f_MK(x,y)
- w = f_WS(x,y)

Since w = r XOR m, every DNA base satisfies the exact parity constraint

r XOR m XOR w = 0.

Truth table:

- A -> (r,m,w) = (0,0,0)
- G -> (0,1,1)
- C -> (1,0,1)
- T -> (1,1,0)

Therefore the three canonical binary descriptions are not independent. They form the four codewords of a [3,2] single-parity-check code over Z2.

Two consequences follow immediately:

1. **Any two of R/Y, M/K, and W/S reconstruct the full four-state base exactly.**
2. **The third quotient is a deterministic parity relation, not an extra fitted feature.**

This is a direct finite realization of the Reality-Code skeleton `alphabet + parity checks + equivalence classes`: a two-bit logical state is represented by three observable binary partitions constrained by one exact parity equation.

Important interpretive limit: this does not show that biology evolved DNA as an error-correcting code for this reason, nor that the biochemical categories implement a physical stabilizer code. It proves only the algebraic/code-theoretic structure of these canonical partitions under the fixed encoding.

## Corollary — projected complement behavior is forced

For a quotient f, complement toggles its output exactly when f(1,1)=1.

- R/Y: f_RY(1,1)=1 -> complement flips the quotient bit.
- M/K: f_MK(1,1)=1 -> complement flips the quotient bit.
- W/S: f_WS(1,1)=1 XOR 1 = 0 -> complement preserves the quotient bit.

Therefore for a DNA sequence, reverse-complement acts as:

- R/Y: reverse + bit flip
- M/K: reverse + bit flip
- W/S: reverse only

This is exactly the transformation rule independently frozen in RCX-LCX-0001 before the Stage-A prevalence-matched null result was interpreted.

## Why this is a legitimate bridge

Reality-Code operates on observation-equivalence classes, quotient maps, parity/check relations, hidden-state non-identifiability, and involutive/symmetry operations. LIFE-CODE operates on the four-state DNA alphabet and exact sequence transfer.

BRIDGE-0001 proves that the canonical DNA reduction maps are mathematically identical in type to the quotient operators required by Reality-Code: the full state alphabet V is mapped to lower-resolution observational equivalence classes by homomorphisms, the three canonical one-bit views obey an exact parity constraint, and complement/reverse-complement acts as a deterministic involution whose action descends to those quotients.

This establishes a shared **formal architecture** between the projects without using biological annotations, fitted parameters, EXP-0003 outcomes, or a retrospective encoding search.

## What this does NOT establish

BRIDGE-0001 does not establish that:

- DNA and physical law share a literal substrate;
- Reality-Code is a fundamental law of physics;
- the quotient maps are biologically selected because of this algebra;
- quotienting improves phylogenetic transfer;
- any simulation/computation ontology is true.

Those require empirical tests. EXP-0003 remains the preregistered biological transfer test.

## Falsifiability / auditability

This formal claim is finite and exhaustively checkable over the four DNA symbols. An executable verifier is stored at `cloud/scripts/bridge0001_verify.py`.
