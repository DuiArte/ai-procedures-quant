"""publish_artifact.py — the sanitization chokepoint.

Turns one private internal report into (public_text, manifest).
Fail-closed: if a blocking rule fires, NO public artifact is written and the
caller must redact the source first. Restraint principle in code.

IMPORTANT: the identity denylist (the personal tokens to catch) is loaded from a
PRIVATE, gitignored file — it is NOT hardcoded here, because hardcoding it would
publish the very terms it exists to hide. Copy `identity_denylist.example.txt` to
`identity_denylist.txt` (gitignored) and fill in the real terms.

MIT-licensed; safe to publish because publishing-safely is its whole job.
"""
from __future__ import annotations
import os
import re
from dataclasses import dataclass, field

# --- Private roots that must never appear in a public artifact --------------
PRIVATE_PATHS = re.compile(
    r"Trading_Index|Account_Archive|SignalLib|[A-Za-z]:\\Users", re.I
)

# --- Bare currency / notional figures (flag, redact to a band) --------------
CURRENCY = re.compile(r"[$€£]\s?\d[\d,]*(?:\.\d+)?|\b\d{4,}(?:\.\d+)?\s?(?:USD|EUR|MXN)\b")

# --- Tickers: only the allow-list survives; others become placeholders ------
TICKER_ALLOWLIST = {"SPX", "ACWI", "AGG", "GLD"}  # published benchmarks only
TICKER = re.compile(r"\b[A-Z]{2,5}\b")

# --- Identity denylist: loaded from a PRIVATE file, never hardcoded ---------
DENYLIST_PATH = os.environ.get("IDENTITY_DENYLIST", "identity_denylist.txt")


def load_identity_regex(path: str = DENYLIST_PATH):
    """Compile an identity regex from a private denylist file.

    One term per line, '#' for comments. Falls back to the shipped example
    (placeholders only). Returns (compiled_regex_or_None, source_path_or_None).
    """
    for candidate in (path, "identity_denylist.example.txt"):
        try:
            with open(candidate, encoding="utf-8") as fh:
                terms = [ln.strip() for ln in fh
                         if ln.strip() and not ln.startswith("#")]
        except FileNotFoundError:
            continue
        if terms:
            return re.compile("|".join(re.escape(t) for t in terms), re.I), candidate
    return None, None


@dataclass
class Manifest:
    redactions: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)

    def note(self, kind: str, detail: str) -> None:
        self.redactions.append(f"{kind}: {detail}")

    def block(self, kind: str, detail: str) -> None:
        self.blockers.append(f"{kind}: {detail}")

    @property
    def clean(self) -> bool:
        return not self.blockers

    def render(self) -> str:
        lines = ["# Redaction manifest", ""]
        lines.append(f"- redactions applied: {len(self.redactions)}")
        lines.append(f"- blockers (must fix before publish): {len(self.blockers)}")
        if self.blockers:
            lines += ["", "## BLOCKERS — publish refused"]
            lines += [f"- {b}" for b in self.blockers]
        if self.redactions:
            lines += ["", "## Redactions applied"]
            lines += [f"- {r}" for r in self.redactions]
        return "\n".join(lines)


def publish_artifact(private_text: str, *, placeholder_tickers: bool = True
                     ) -> tuple[str | None, Manifest]:
    """Return (public_text, manifest).

    public_text is None when a blocking rule fires — fail-closed.
    """
    m = Manifest()
    text = private_text

    # 0. Load the private identity denylist. No denylist => refuse (fail-closed):
    #    publishing without identity scanning is never safe.
    identity, source = load_identity_regex()
    if identity is None:
        m.block("config", "no identity denylist found — refusing to publish")
        return None, m

    # 1. Blocking scans — these refuse publication outright.
    for hit in set(identity.findall(text)):
        # allow a denied term only when it sits inside a benign phrase such as
        # the proper noun "Monte Carlo" (the one whitelisted collision)
        if f"monte {hit}".lower() in text.lower():
            continue
        m.block("identity", hit)
    for hit in set(PRIVATE_PATHS.findall(text)):
        m.block("private-path", hit)

    # 2. Currency / notional — redact to a band, record it.
    def _band(match: re.Match) -> str:
        m.note("currency", match.group(0))
        return "[REDACTED:notional]"
    text = CURRENCY.sub(_band, text)

    # 3. Tickers — placeholder anything off the allow-list.
    if placeholder_tickers:
        seen: dict[str, str] = {}
        def _ph(match: re.Match) -> str:
            t = match.group(0)
            if t in TICKER_ALLOWLIST:
                return t
            if t not in seen:
                seen[t] = f"ASSET_{chr(ord('A') + len(seen))}"
                m.note("ticker", f"{t} -> {seen[t]}")
            return seen[t]
        text = TICKER.sub(_ph, text)

    if not m.clean:
        return None, m          # fail-closed: caller must redact the source
    return text, m


if __name__ == "__main__":
    import sys
    src = sys.stdin.read()
    public, manifest = publish_artifact(src)
    sys.stderr.write(manifest.render() + "\n")
    if public is None:
        sys.exit("REFUSED: blockers present — redact source and retry.")
    sys.stdout.write(public)
