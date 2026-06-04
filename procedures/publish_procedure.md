# Procedure · Publish (the gate)

**Goal:** turn a private internal report into a public artifact without leaking the
edge. This is the chokepoint procedure.

**Inputs:** `<private_report>`.

**Preconditions / gates:**
- [ ] the source is a *final* report, not a work-in-progress
- [ ] the target repo and license are decided

## Steps

1. **Generate** the private report.
2. **Sanitize:** `cat <private_report> | python examples/publish_artifact.py`
   → public text + redaction manifest. *Fail-closed:* a blocker aborts with no output.
3. **Diff** the public text vs the last published version.
4. **Approve (human):** read the diff + manifest; reject if the thesis is too
   revealing or a stat is too precise. Rejection returns the artifact to private.
5. **Commit** to the public repo draft; run the leak scan against the **private**
   identity denylist (`identity_denylist.txt`, gitignored — never list the real
   terms in a shipped file).
6. **Tag** the release.
7. **Card:** update the site's `projects.json`.

## Outputs

- public artifact + redaction manifest

## Failure handling

| Failure | Detection | Action |
|---|---|---|
| blocker fired | sanitizer returns no output | redact the *source*, never loosen the rule |
| half-published | repo updated, card not | commit repo first, card last; missing card is the safe state |
| post-publish leak | leak scan after push | `git revert` + treat value as compromised (a push is irreversible in practice) |

> Terse: `GEN && ANL @sanitize && RPT >diff && DEP || RDC`
