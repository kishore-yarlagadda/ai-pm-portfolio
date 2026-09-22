"""Static integrity checks for canonical evidence-preserving PM templates."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "templates"
CANONICAL = {
    "discovery_template.md",
    "strategy_template.md",
    "prd_template.md",
}
DEPRECATED_DUPLICATES = {"discovery.md", "strategy.md", "prd.md"}

# These were unsupported generated claims/placeholders in the defective artifacts.
# Keep this list narrow enough that templates can discuss the general concepts safely.
FORBIDDEN = {
    "Date: Today": "use an ISO date backed by evidence, or UNKNOWN",
    "two-week estimate": "cite an approved estimate source, or preserve UNKNOWN",
    "RICE score": "do not hard-code an unsourced prioritization score",
    "100% adoption": "do not invent an adoption target",
    "zero unaudited deployments": "do not invent a control target or imply deployments",
    "50% reduction": "do not invent a quantitative target",
}

# Common fabricated values from generated PM artifacts. Extend with incident-specific
# phrases when a regression is found; do not ban neutral field names such as Owner.
FORBIDDEN_PATTERNS = {
    r"(?im)^\s*(?:status|owner|persona|stakeholder)\s*:\s*(?!\[|`?UNKNOWN\b|$).+":
        "hard-coded control/person values require evidence",
    r"(?im)^\s*(?:estimate|timeline|duration)\s*:\s*(?:2\s*weeks?|two\s*weeks?)\s*$":
        "hard-coded duration requires an approved estimate source",
    r"(?i)\barchitecture\.md\b":
        "do not link to or assert a generic architecture artifact unless it exists",
}

MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def markdown_files() -> list[Path]:
    return sorted(TEMPLATE_DIR.glob("*.md"))


def test_exactly_one_canonical_template_per_artifact() -> None:
    names = {path.name for path in markdown_files()}
    assert CANONICAL <= names, f"Missing canonical templates: {sorted(CANONICAL - names)}"
    assert not (names & DEPRECATED_DUPLICATES), (
        "Remove duplicate aliases rather than allowing two editable sources: "
        f"{sorted(names & DEPRECATED_DUPLICATES)}"
    )


def test_no_known_unsupported_claims_or_placeholders() -> None:
    failures: list[str] = []
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for phrase, remedy in FORBIDDEN.items():
            if phrase.casefold() in text.casefold():
                failures.append(f"{path.name}: forbidden {phrase!r}; {remedy}")
        for pattern, remedy in FORBIDDEN_PATTERNS.items():
            for match in re.finditer(pattern, text):
                line = text.count("\n", 0, match.start()) + 1
                failures.append(
                    f"{path.name}:{line}: forbidden pattern {pattern!r}; {remedy}"
                )
    assert not failures, "\n" + "\n".join(failures)


def _relative_target(raw_target: str) -> str | None:
    target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or target.startswith(("#", "mailto:", "tel:")):
        return None
    return unquote(parsed.path)


def test_relative_markdown_links_resolve() -> None:
    failures: list[str] = []
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK.finditer(text):
            relative = _relative_target(match.group(1))
            if not relative:
                continue
            destination = (path.parent / relative).resolve()
            try:
                destination.relative_to(ROOT.resolve())
            except ValueError:
                failures.append(f"{path.name}: link escapes repair root: {match.group(1)!r}")
                continue
            if not destination.exists():
                line = text.count("\n", 0, match.start()) + 1
                failures.append(
                    f"{path.name}:{line}: broken relative link {match.group(1)!r}"
                )
    assert not failures, "\n" + "\n".join(failures)

if __name__ == "__main__":
    test_exactly_one_canonical_template_per_artifact()
    test_no_known_unsupported_claims_or_placeholders()
    test_relative_markdown_links_resolve()
    print("3 template integrity checks passed")
