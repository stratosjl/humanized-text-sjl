#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
greek_text_check.py — PreToolUse hook for Claude Code (Linux / macOS / Windows).

Blocks Write/Edit operations on .md / .txt files when the inserted text
contains:

  1. em dashes (U+2014) or en dashes (U+2013)
  2. Greek "Oxford comma" before "και"  (Rule §7 of humanized-text-sjl)
  3. English semicolon used as άνω τελεία (Rule §8)
  4. Hard-block English terms that have a Greek substitute
     (anti-anglicism, Rule §11)
  5. Greek-to-Greek preferred-term violations (Rule §16),
     e.g. «εκκρεμές» → «σε εκκρεμότητα»,
          «διάδρομος επικοινωνίας» → «κανάλι επικοινωνίας»

International technical acronyms (MiFID, DORA, GDPR, AML, etc.) are
whitelisted via INTL_ACRONYMS. Lines that look like regulatory citations
(>= 80% Latin chars OR an explicit citation marker) are skipped for the
word-level checks; the dash/comma rules still apply.

Soft (advisory-only) finding:
  - parathesis heuristic for "<EnglishToken> <GreekNoun>" anglicism,
    surfaced but not blocking.

Exit codes:
  0  passed (no violations) or non-applicable tool/path
  2  hard violations found, blocked back to Claude (stderr message)

Configuration via environment variables (all optional):

  HUMANIZED_TEXT_ENFORCE_ROOTS
      Comma-separated list of path substrings (case-sensitive). The hook
      ONLY enforces on file paths containing at least one of these. Default:
      empty (= enforce on every .md/.txt write that is not exempt).

  HUMANIZED_TEXT_EXEMPT_SEGMENTS
      Comma-separated list of path substrings to skip. Default:
      "/memory/,/.claude/,/.git/,/node_modules/,/Plugins/,/HANDOVER".

  HUMANIZED_TEXT_ENFORCE_OVERRIDES
      Comma-separated list of path substrings that re-enable enforcement
      even when an EXEMPT_SEGMENTS rule would otherwise skip. Use this for
      operator-owned plugin marketplaces under ~/.claude/plugins/ where
      regulator-presentable CHANGELOG / README prose lives. Default covers
      the common stratosjl-owned marketplaces; extend via env-var for your
      own. Match is plain substring after Windows backslash normalisation,
      so Linux/macOS/Windows paths are handled uniformly.

Install: see scripts/INSTALL.md in the humanized-text-sjl repo.
"""
from __future__ import annotations

import io
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# Force UTF-8 on stdin/stdout/stderr. Critical on Windows (cp1252 default
# mangles Greek text and turns multibyte UTF-8 sequences into spurious
# em-dash detections). Harmless on macOS/Linux, which are already UTF-8.
# ---------------------------------------------------------------------------
try:
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

EM_DASH = "—"
EN_DASH = "–"

# Pattern: ", και" — Oxford comma in Greek, banned by humanized-text Rule §7.
COMMA_KAI_RE = re.compile(r",\s+και\b")

# Pattern: ";" followed by space and a lowercase Greek letter — almost
# certainly an English-style semicolon misused as άνω τελεία (Rule §8).
INNER_SEMICOLON_RE = re.compile(r";\s+[α-ωάέήίόύώ]")


def _env_list(name: str, default: tuple[str, ...]) -> tuple[str, ...]:
    raw = os.environ.get(name)
    if raw is None:
        return default
    parts = tuple(p.strip() for p in raw.split(",") if p.strip())
    return parts


# By default the hook enforces on EVERY .md/.txt write that is not in an
# exempt segment. Set HUMANIZED_TEXT_ENFORCE_ROOTS to restrict to specific
# project sub-trees (e.g. team or client folders).
ENFORCE_ROOTS = _env_list("HUMANIZED_TEXT_ENFORCE_ROOTS", ())

EXEMPT_SEGMENTS = _env_list(
    "HUMANIZED_TEXT_EXEMPT_SEGMENTS",
    (
        "/memory/",
        "/.claude/",
        "/.git/",
        "/node_modules/",
        "/Plugins/",
        "/HANDOVER",
    ),
)

# Re-enforce overrides. Path substrings that, when present, force the hook to
# enforce even though one of the EXEMPT_SEGMENTS would otherwise exempt the
# file. Use this for operator-owned plugin marketplaces under ~/.claude/plugins/
# where the operator authors regulator-presentable CHANGELOG / README prose.
# Match is a plain substring after path normalisation (Windows backslashes
# rewritten to forward slashes), so the same rules work on Linux, macOS, and
# Windows. Case-sensitive by design (filesystem paths under operator control
# are typically stable in case).
ENFORCE_OVERRIDES = _env_list(
    "HUMANIZED_TEXT_ENFORCE_OVERRIDES",
    (
        "/.claude/plugins/marketplaces/vibe-coding-rules/",
        "/.claude/plugins/marketplaces/stratosjl-design-engineering/",
        "/.claude/plugins/marketplaces/humanized-text-sjl/",
    ),
)

CHECK_EXTENSIONS = (".md", ".txt")

# HARD-BLOCK terms. Each appearance flags the file unless inside a
# whitelisted citation line.
HARD_BLOCK = {
    "canonical": "εγκυρότερη / αναφορική / επίσημη",
    "bilateral": "διμερής (όχι «αμφίπλευρος» — bilateral relations = διμερείς σχέσεις)",
    "multilateral": "πολυμερής",
    "unilateral": "μονομερής",
    "artifacts": "κείμενα / έντυπα",
    "artifact": "κείμενο / έντυπο",
    "consent": "συναίνεση",
    "attestation": "βεβαίωση",
    "warranty": "εγγύηση",
    "Conditions Precedent": "Προαπαιτούμενα",
    "escalation": "κλιμάκωση",
    "softened": "μαλακότερη / ηπιότερη",
    "softer": "μαλακότερη / ηπιότερη",
    "tighten": "αυστηροποίηση",
    "rollback": "επαναφορά",
    "fallback": "εφεδρική επιλογή",
    "covenant": "ρήτρα",
    "redline": "παρατήρηση επί του κειμένου",
    "trigger": "ενεργοποίηση",
    "carve-out": "εξαίρεση",
    "carveout": "εξαίρεση",
    "scope": "πεδίο / εύρος",
}

# GREEK-to-GREEK preferred-term hard blocks (Rule §16 in humanized-text-sjl
# SKILL.md). Pattern is matched with a Greek-aware non-letter lookaround;
# case-sensitive on Greek letters because Greek inflection makes
# case-folding lossy. Keep entries narrow to avoid flagging legitimate uses
# of cognate words (e.g. "εκκρεμότητα", "εκκρεμή χρέη").
GREEK_HARD_BLOCK = {
    "εκκρεμές":               "σε εκκρεμότητα (Rule §16: μην χρησιμοποιείς το «εκκρεμές» ως κατηγορούμενο)",
    "διάδρομος επικοινωνίας": "κανάλι επικοινωνίας (Rule §16: «διάδρομος επικοινωνίας» είναι calque)",
    "διαδρόμου επικοινωνίας": "καναλιού επικοινωνίας (Rule §16)",
    "διάδρομο επικοινωνίας":  "κανάλι επικοινωνίας (Rule §16)",
    "να είμαι καθαρός":       "για να είμαι σαφής (Rule §16: «να είμαι καθαρός» είναι calque του «let me be clear»)",
    "Να είμαι καθαρός":       "Για να είμαι σαφής (Rule §16: calque του «let me be clear»)",
    "να είμαι καθαρή":        "για να είμαι σαφής (Rule §16)",
    "Να είμαι καθαρή":        "Για να είμαι σαφής (Rule §16)",
    "να είμαστε καθαροί":     "για να είμαστε σαφείς (Rule §16)",
    "Να είμαστε καθαροί":     "Για να είμαστε σαφείς (Rule §16)",
    "να γίνω καθαρός":        "για να είμαι σαφής (Rule §16)",
    "είναι καθαρό ότι":       "είναι σαφές ότι / είναι ξεκάθαρο ότι (Rule §16: «είναι καθαρό ότι» είναι calque του «it's clear that»)",
    "Είναι καθαρό ότι":       "Είναι σαφές ότι / Είναι ξεκάθαρο ότι (Rule §16: calque του «it's clear that»)",
    "είναι καθαρό πως":       "είναι σαφές πως / είναι ξεκάθαρο πως (Rule §16)",
    "Είναι καθαρό πως":       "Είναι σαφές πως / Είναι ξεκάθαρο πως (Rule §16)",
    "ήταν καθαρό ότι":        "ήταν σαφές ότι / ήταν ξεκάθαρο ότι (Rule §16)",
    "Ήταν καθαρό ότι":        "Ήταν σαφές ότι / Ήταν ξεκάθαρο ότι (Rule §16)",
    "γίνεται καθαρό ότι":     "γίνεται σαφές ότι (Rule §16)",
}

# TECHNICAL TERMS allowed in Greek prose. NOT in the block list. Listed
# here for documentation: reviewers should still prefer Greek substitutes
# where natural, but these may stay English when they carry MiFID II /
# DORA / EBA technical meaning, especially in regulatory citations.
TECH_ALLOWED = (
    "outsourcing",
    "audit trail",
    "letterbox",
    "retrocession",
    "tipping-off",
    "thematic review",
    "threshold",
    "best execution",
    "due diligence",
    "investment advice",
    "compliance",
    "share",
    "split",
    "fee",
    "fees",
)

INTL_ACRONYMS = frozenset(
    {
        "HCMC", "ESMA", "EBA", "EIOPA", "ECB", "EU", "EE", "FINMA",
        "MiFID", "MiFIR", "MAR", "EMIR", "DORA", "GDPR", "AIFMD", "AIF",
        "SFDR", "PRIIPs", "MiCA", "NIS2", "FATCA", "CRS", "RIS", "AI",
        "AML", "AMLRO", "DPO", "QET", "ICT", "RoI", "KPI", "ESG", "RTO",
        "DPM", "EAM", "PFOF", "PEP", "RTS", "ITS", "IBAN", "OMS", "PMS",
        "UBS", "ADEPA", "CSSF", "BIC", "ISIN",
        "SI", "OTC", "ELTIF", "UCITS", "CDD", "EDD", "KYC", "ID",
        "FINSA", "CSA", "CFD", "ICAAP", "ICARA", "FATF", "OFAC",
        "URL", "PDF", "API",
    }
)

LATIN_CHAR = re.compile(r"[A-Za-z]")
GREEK_CHAR = re.compile(r"[Α-Ωα-ωΆΈΉΊΌΎΏΪΫϊϋΐΰάέήίόύώ]")
LATIN_TOKEN = r"[A-Za-z][A-Za-z0-9\-_]{1,}"
GREEK_TOKEN = r"[Α-Ωα-ωΆΈΉΊΌΎΏΪΫϊϋΐΰάέήίόύώ]+"
PARATHESIS_RE = re.compile(rf"(?P<eng>{LATIN_TOKEN})\s+(?P<gr>{GREEK_TOKEN})")

# Greek stop-words / non-noun particles. If a Latin token is followed by
# one of these, it is NOT a parathesis anglicism (it is a normal sentence
# transition).
GREEK_STOP_WORDS = frozenset(
    {
        "και", "είναι", "ως", "με", "για", "του", "της", "των", "ή", "στο",
        "στη", "στην", "στους", "στις", "στα", "σε", "από", "μετά", "πριν",
        "πάνω", "κάτω", "μέσα", "έξω", "παρά", "χωρίς", "αν", "ότι", "ώστε",
        "γιατί", "διότι", "επειδή", "όταν", "όποτε", "έχει", "θα", "να",
        "δεν", "δε", "μη", "μην", "που", "ποιος", "πού", "πότε", "πώς",
        "μόνο", "ίδιο", "λόγω", "βάσει", "κατά", "μεταξύ", "αντί",
        "κάθε", "κάποιος", "κάποιον", "κάποια", "κάποιο", "λοιπόν", "ωστόσο",
        "παρόλο", "πλέον", "πάλι", "ακόμη", "ακόμα", "πολύ", "λίγο", "πιο",
        "θεωρούνται", "θεωρείται", "θεωρούν", "παραμένουν", "παραμένει",
        "ενημερώνεται", "ενημερώνονται", "ισχύει", "ισχύουν", "πληρούται",
        "καθορίζεται", "οριζόμενα", "ορίζεται", "ορίζονται", "αποτελεί",
        "αποτελούν", "αναφέρει", "αναφέρεται", "αναφέρονται", "ζητείται",
        "ζητούν", "διαβιβάζει", "διαβιβάζεται", "διέπει", "διέπεται",
    }
)

# Greek company suffixes/legal-form tokens (single letter or short).
GREEK_COMPANY_SUFFIXES = frozenset({"Α", "ΑΕ", "Α.Ε", "Α.Ε.", "Ε", "ΕΠΕ", "ΟΕ", "ΕΕ"})

# Markers that identify a citation/source line; if found, line is skipped.
CITATION_MARKERS = (
    "EBA/GL", "ESMA/", "ESMA-", "ESMA35", "ESMA/2", "ESMA Supervisory",
    "Regulation (EU)", "Directive 20", "Κανονισμός (ΕΕ)", "Οδηγία 20",
    "FINMA Circular", "FINSA", "(ESMA", "(EBA", "(EU)", "BCBS",
    "Πράξη Εκτελεστικής", "Π.Ε.Ε.", "ΦΕΚ", "Ν. 4514/2018",
    "Ν. 4557/2018", "Ν. 5193/2025", "Κατ' Εξουσιοδότηση",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _norm(p: str) -> str:
    """Normalise Windows backslashes to forward slashes for substring tests."""
    return p.replace("\\", "/")


def is_enforced_path(path: str) -> bool:
    if not path:
        return False
    p = _norm(path)
    if not p.endswith(CHECK_EXTENSIONS):
        return False
    # Re-enforce overrides win over EXEMPT_SEGMENTS. This is how operator-
    # owned plugin marketplaces under ~/.claude/plugins/ get enforced even
    # though the path contains "/.claude/", which would normally exempt it.
    if any(override in p for override in ENFORCE_OVERRIDES):
        return True
    if any(seg in p for seg in EXEMPT_SEGMENTS):
        return False
    if not ENFORCE_ROOTS:
        return True
    return any(root in p for root in ENFORCE_ROOTS)


def _is_citation_line(line: str) -> bool:
    """
    Heuristic: skip lines whose content is dominated by Latin characters
    (regulatory titles, English source names) or that contain explicit
    citation markers. We still scan such lines for em/en dashes.
    """
    stripped = line.strip()
    if not stripped:
        return True
    if any(marker in stripped for marker in CITATION_MARKERS):
        return True

    latin = len(LATIN_CHAR.findall(stripped))
    greek = len(GREEK_CHAR.findall(stripped))
    total_letters = latin + greek
    if total_letters >= 8 and latin / total_letters >= 0.8:
        return True
    return False


def _strip_code_fences(text: str) -> str:
    out_lines = []
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            out_lines.append("")
            continue
        if in_fence:
            out_lines.append("")
        else:
            out_lines.append(line)
    return "\n".join(out_lines)


def _strip_inline_code(line: str) -> str:
    return re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line)


def _strip_parentheses(line: str) -> str:
    """Mask ASCII () groups and Greek « » pairs to silence terms in apposition."""
    line = re.sub(r"\([^()]*\)", lambda m: " " * len(m.group(0)), line)
    line = re.sub(r"«[^»]*»", lambda m: " " * len(m.group(0)), line)
    return line


def find_violations(text: str) -> list[dict]:
    """
    Returns a flat list of issues; each issue carries a 'severity' field:
      - 'hard'  -> blocking (em/en dash, hard-block terms)
      - 'soft'  -> advisory only (parathesis heuristic)

    Callers decide whether to block based on severity.
    """
    issues: list[dict] = []
    text = _strip_code_fences(text)
    for i, raw_line in enumerate(text.splitlines(), start=1):
        # Em / en dashes are checked even in citation lines (banned everywhere).
        if EM_DASH in raw_line:
            issues.append(
                {"line": i, "kind": "em_dash", "severity": "hard",
                 "msg": "em dash (—)", "snip": raw_line.strip()}
            )
        if EN_DASH in raw_line:
            issues.append(
                {"line": i, "kind": "en_dash", "severity": "hard",
                 "msg": "en dash (–)", "snip": raw_line.strip()}
            )
        if COMMA_KAI_RE.search(raw_line):
            issues.append(
                {"line": i, "kind": "comma_kai", "severity": "hard",
                 "msg": "', και' -> ' και' (Rule §7: όχι κόμμα πριν το «και»)",
                 "snip": raw_line.strip()}
            )
        if INNER_SEMICOLON_RE.search(raw_line):
            issues.append(
                {"line": i, "kind": "inner_semicolon", "severity": "hard",
                 "msg": "';' σε ελληνικό κείμενο -> άνω τελεία '·' (Rule §8)",
                 "snip": raw_line.strip()}
            )

        # Skip citation-style lines for word-level checks.
        if _is_citation_line(raw_line):
            continue

        scan = _strip_inline_code(raw_line)
        scan_unparen = _strip_parentheses(scan)

        # Hard-block English terms (case-insensitive, Latin word boundary).
        for term, sub in HARD_BLOCK.items():
            pattern = re.compile(
                r"(?<![A-Za-z])" + re.escape(term) + r"(?![A-Za-z])",
                re.IGNORECASE,
            )
            if pattern.search(scan_unparen):
                issues.append(
                    {
                        "line": i,
                        "kind": "banned_term",
                        "severity": "hard",
                        "msg": f"'{term}' -> {sub}",
                        "snip": raw_line.strip(),
                    }
                )

        # Greek-to-Greek preferred terms (Rule §16). Greek-aware non-letter
        # lookaround so "εκκρεμές" matches but "εκκρεμότητα" does not.
        for term, sub in GREEK_HARD_BLOCK.items():
            pattern = re.compile(
                r"(?<![Α-Ωα-ωΆ-Ώά-ώϊϋΐΰ])" + re.escape(term) + r"(?![Α-Ωα-ωΆ-Ώά-ώϊϋΐΰ])",
            )
            if pattern.search(scan_unparen):
                issues.append(
                    {
                        "line": i,
                        "kind": "greek_preferred_term",
                        "severity": "hard",
                        "msg": f"'{term}' -> {sub}",
                        "snip": raw_line.strip(),
                    }
                )

        # Parathesis anglicism heuristic — SOFT (advisory), not blocking.
        # Many false positives are unavoidable without a Greek POS tagger,
        # so we surface them but do not fail the write.
        for m in PARATHESIS_RE.finditer(scan_unparen):
            eng = m.group("eng")
            gr = m.group("gr")
            if eng in INTL_ACRONYMS:
                continue
            if eng.lower() in {t.lower() for t in TECH_ALLOWED}:
                continue
            if re.fullmatch(r"[A-Za-z]{1,2}\d+", eng):
                continue
            if re.fullmatch(r"[A-Z]\d", eng):
                continue
            if gr.lower() in GREEK_STOP_WORDS:
                continue
            if gr in GREEK_COMPANY_SUFFIXES or len(gr) <= 2:
                continue
            issues.append(
                {
                    "line": i,
                    "kind": "parathesis",
                    "severity": "soft",
                    "msg": f"παράθεση(?): '{eng} {gr}' — έλεγξε αν χρειάζεται αναδιάταξη",
                    "snip": raw_line.strip(),
                }
            )

    return issues


def _read_payload() -> dict | None:
    raw = sys.stdin.read()
    if not raw.strip():
        return None
    try:
        return json.loads(raw)
    except Exception:
        return None


def _standalone_scan(target: str) -> int:
    """Standalone CLI mode: scan a file path and print findings to stdout."""
    if not os.path.isfile(target):
        print(f"[err] not a file: {target}", file=sys.stderr)
        return 2
    with open(target, encoding="utf-8") as f:
        content = f.read()
    issues = find_violations(content)
    hard = [v for v in issues if v.get("severity") == "hard"]
    soft = [v for v in issues if v.get("severity") == "soft"]
    if not issues:
        print(f"[ok] no violations in {target}")
        return 0
    if hard:
        print(f"[BLOCK] {len(hard)} hard violation(s) in {target}:")
        for v in hard:
            print(f"  line {v['line']:>4} [{v['kind']}]: {v['msg']}")
            print(f"           > {v['snip'][:140]}")
    if soft:
        print(f"\n[warn] {len(soft)} soft (parathesis) finding(s) — review manually:")
        for v in soft:
            print(f"  line {v['line']:>4} [{v['kind']}]: {v['msg']}")
            print(f"           > {v['snip'][:140]}")
    return 2 if hard else 0


def main() -> int:
    if len(sys.argv) >= 2 and sys.argv[1] == "--standalone":
        if len(sys.argv) < 3:
            print("usage: greek_text_check.py --standalone <file>", file=sys.stderr)
            return 2
        return _standalone_scan(sys.argv[2])

    payload = _read_payload()
    if not payload:
        return 0

    tool = payload.get("tool_name", "")
    inp = payload.get("tool_input", {}) or {}

    if tool == "Write":
        path = inp.get("file_path", "")
        content = inp.get("content", "")
    elif tool == "Edit":
        path = inp.get("file_path", "")
        content = inp.get("new_string", "")
    else:
        return 0

    if not is_enforced_path(path):
        return 0

    issues = find_violations(content)
    hard = [v for v in issues if v.get("severity") == "hard"]
    if not hard:
        return 0

    sys.stderr.write(
        "BLOCKED by humanized-text-sjl greek_text_check: εντοπίστηκαν σκληρές "
        "παραβιάσεις στους κανόνες ελληνικού κειμένου στο αρχείο:\n"
    )
    sys.stderr.write(f"  {path}\n\n")
    for v in hard[:40]:
        sys.stderr.write(f"  line {v['line']:>4} [{v['kind']}]: {v['msg']}\n")
        snip = v["snip"][:140]
        sys.stderr.write(f"           > {snip}\n")
    if len(hard) > 40:
        sys.stderr.write(f"  ... και άλλες {len(hard) - 40} σκληρές παραβιάσεις\n")
    sys.stderr.write(
        "\n"
        "Διόρθωσε ΟΛΕΣ τις παραπάνω εγγραφές πριν ξανατρέξεις Write/Edit. "
        "Αναφορά: humanized-text-sjl SKILL.md (Rules §7, §8, §11, §16).\n"
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
