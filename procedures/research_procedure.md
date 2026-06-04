# Procedure · Research

**Goal:** investigate an idea from hypothesis to go/no-go without fooling yourself.

**Inputs:** `<hypothesis>`, `<data>` (placeholders).

**Preconditions / gates:**
- [ ] hypothesis stated *before* looking at the data
- [ ] a pre-registered success criterion

## Steps

1. State the economic rationale (publishable) separately from the parameters (private).
2. Build the feature/screen using the
   [signallib-framework](https://github.com/DuiArte/signallib-framework) interfaces.
3. Test in-sample, then out-of-sample; keep the search log **private**.
4. Decide: promote to a strategy, shelve, or kill.

## Outputs

- a one-page finding (rationale public, parameters private)

## Failure handling

| Failure | Detection | Action |
|---|---|---|
| hindsight fitting | criterion moved after seeing results | discard the run |
| multiple-testing | many features tried, one "worked" | adjust for trials / PBO |

> Terse: `ANL @file:<data> && SCR && RPT >md`
