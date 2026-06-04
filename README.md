<sub>**DuiArte** · quantitative research · [methodology](https://github.com/DuiArte/ltcma-methodology) · [strategies](https://github.com/DuiArte/static-drift-weight) · [framework](https://github.com/DuiArte/signallib-framework)</sub>

# AI Procedures · Quant

**Sanitized, reusable operating procedures for AI-assisted quant research — the shape of the workflow, with the operating specifics stripped out.**

![status](https://img.shields.io/badge/status-stable-blue) ![license](https://img.shields.io/badge/license-CC--BY--4.0-green) ![updated](https://img.shields.io/badge/updated-2026--06-lightgrey)

---

This repository publishes templated versions of the `AI_PROCEDURES` used to run
backtests, research, and publishing — with every broker, account, path, and
parameter replaced by a placeholder. It also ships the reference sanitizer,
[`examples/publish_artifact.py`](examples/publish_artifact.py), the helper that turns
a private report into a public artifact plus a redaction manifest.

## What's here

- **`procedures/`** — templated procedures (backtest, research, publish) with
  parameters left as `<placeholders>`.
- **`templates/procedure_template.md`** — the blank template to author a new
  procedure.
- **`examples/publish_artifact.py`** — the sanitization chokepoint, MIT-licensed; safe
  to publish because publishing-safely is its whole job.

## What's deliberately *not* here

Any procedure step naming a real broker, account, credential, private file path, or
specific parameter value; anything revealing the live trading cadence. See
[`_MANIFEST.md`](_MANIFEST.md).

## Using the sanitizer

```bash
cat private_report.md | python examples/publish_artifact.py > public_report.md
# the redaction manifest is written to stderr; a blocker aborts with no output
```

## License

[CC BY-4.0](LICENSE) for the procedures/templates (adapt freely, with attribution).
`examples/publish_artifact.py` is MIT (see its header).
