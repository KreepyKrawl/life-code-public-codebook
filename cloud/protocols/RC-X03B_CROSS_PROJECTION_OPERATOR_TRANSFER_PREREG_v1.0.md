# RC-X03B — Cross-Projection Operator Transfer Preregistration v1.0

Status: **FROZEN BEFORE TARGET-COMPOSITION REVEAL**

Purpose: empirical test of BRIDGE-0008. Determine whether an operation algebra frozen in source domain A transfers to target domain B under one frozen cross-domain mapping C, such that unseen target compositions are predicted without composition-specific fitting.

## Hypothesis

There exists one latent operation algebra G represented in two observed domains A and B such that, on the tested state manifold,

`T_B(g) = C o T_A(g) o C^-1`

for the frozen primitive generators and their held-out compositions.

This is an empirical shared-algebra hypothesis. It does not by itself assert literal substrate identity.

## Freeze boundary

Before revealing any target-domain held-out composition outcomes, freeze:

1. source-domain primitive generators g1,g2,g3 and their full available intervention trajectories;
2. source-domain composition algebra, including order dependence and inverse definitions;
3. target-domain calibration set containing primitive interventions only;
4. cross-domain map C and all parameters learned from primitive calibration;
5. preprocessing, state representation, timing normalization, and dimensionless coordinates;
6. scorer and tolerance rules;
7. alternative model classes and their fitting budgets;
8. held-out composition list.

No composition-specific target-domain fitting is permitted after freeze.

## Held-out target tests

Primary held-out words:

- W1 = g2 g1
- W2 = g1 g2
- W3 = g3 g2 g1
- W4 = g1^-1 g2^-1 g1 g2  (commutator loop)

If additional words are added before data reveal, they must be hashed and listed in a versioned amendment before execution.

## Prediction rule

For each held-out word w,

`Pred_B(w) = C o T_A(w) o C^-1`

or the corresponding trajectory-level form if operators are represented dynamically.

All target predictions must be committed before target truth is revealed.

## Primary scoring

Use preregistered trajectory/state error on dimensionless coordinates. At minimum report:

- median normalized prediction error across held-out words;
- p90 normalized error;
- per-word error;
- order-discrimination score comparing W1 vs W2;
- commutator residual for W4;
- uncertainty / replicate dispersion when applicable.

The exact numeric pass thresholds must be taken from the already frozen Reality-Code benchmark family if available. If no threshold is already frozen, thresholds must be frozen from source-domain and primitive-calibration noise only, never from held-out composition truth.

## Required alternative models

Compare the frozen Reality-Code/shared-algebra model against preregistered alternatives with matched calibration access:

1. domain-specific physics model;
2. similarity / renormalization-style mapping;
3. Koopman / operator-learning baseline;
4. causal-bottleneck / emergence baseline;
5. target-local flexible predictor with complexity penalty;
6. null mapping preserving marginal state statistics but destroying composition algebra.

Alternative models may see exactly the same target primitive calibration information as the shared-algebra model and no held-out target composition truth.

## Discriminating criteria

A meaningful empirical pass requires all of the following:

1. the frozen shared-algebra model predicts held-out target compositions within the preregistered tolerance;
2. W1 and W2 are distinguished correctly when source algebra is noncommutative;
3. the commutator-loop prediction is correct within tolerance;
4. performance exceeds the frozen null mapping;
5. the result is not explained equally well by a simpler preregistered baseline under the same calibration budget;
6. no target composition-specific parameter is introduced post-freeze.

## Failure interpretation

Failure falsifies transfer of the particular frozen algebra/map C over the tested domain and state manifold. It does not falsify the formal BRIDGE-0008 theorem and does not by itself falsify Unified Substrate ontology.

## Pass interpretation

Pass establishes cross-domain predictive transfer of a nontrivial operation algebra under a frozen mapping. It elevates the bridge to empirical cross-domain generalization for the tested systems.

It still does not uniquely establish that the systems are literally the same physical substrate realization, because independently isomorphic systems remain logically possible.

## Relation to LIFE-CODE

This protocol is independent of EXP-0003 and must not inspect or use EXP-0003 primary outcomes. LIFE-CODE enters only through already-proved formal bridge results until its own global reveal barrier is lifted.

## Claim boundary

A successful RC-X03B result would justify:

`The same frozen operation algebra predicts unseen compositions across two independently observed domains under one fixed representation map.`

It would not justify, by itself:

`All reality is one discovered code`, `simulation is proven`, `consciousness is the substrate`, or any uniquely specified metaphysical implementation.
