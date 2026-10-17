# Changelog

## 2.3.0 (2026-10-17)

Rule §21, subject and verb agreement where the subject's number must show from its first word, contributed by the operator.

The case: «Η ισχύουσα παρ. 6 του άρθρου 6 του ν. 4209/2013 και η παρ. 4 του άρθρου 12 του ν. 4099/2012 περιλαμβάνουν». Coordination with «και» formally licenses the plural verb, but the reader starts on a singular article, crosses a long chain of genitives, and meets a plural verb that reads as a mismatch. Where the coordinated items share a head noun (παράγραφος, άρθρο, νόμος, απόφαση), the noun is written once in the plural with plural article and modifier, and the numbers follow: «Οι ισχύουσες παρ. 6 ... και 4 ... περιλαμβάνουν». Coordinated items with different heads (country names, for instance) keep the coordination; the rule says so, so that it is not over-applied.

Found in a delivered Greek regulatory report, where the sentence appeared twice, once in a consultation comment. Pass 2 by nature (finding the subject needs reading); `greek-scan.md` carries an indicative row for the common shape. Not wired into `scripts/greek_text_check.py`: a regex for «Η X ... και η X ... <plural verb>» needs a reliable plural-verb test and fixtures in both directions before it could block anything.

## 2.2.0 (2026-09-02)

Rule §20, punctuation with quotation marks, contributed by the operator.

Greek does not follow the American convention of putting the full stop inside the quotes. The position of the mark shows who owns it, the quotation or the main clause, so the wrong position changes the meaning: «Φώναξε δυνατά: "Είμαι παρών!"» is the speaker shouting, while «Ποιος είπε τη φράση "είμαι παρών";» is the writer asking. Three parts: the full stop always sits outside; the exclamation and question marks sit inside when they belong to the quoted text and outside when they belong to the main clause; and two terminal marks never combine, so an inner `!` or `;` suppresses the outer full stop.

Only the third part is mechanically decidable, and only that part went into `greek-scan.md`. Deciding where the mark belongs requires knowing whether it is the quotation speaking or the writer, which no pattern can see, so §20.1 and §20.2 are Pass 2 and stay with the reader. The reference says so on its face rather than leaving the next author to discover that a scan cannot enforce two thirds of the rule.

Not yet wired into `scripts/greek_text_check.py`. Doing so would move §20.3 from a documented rule to an enforced one, which is where this skill's rules belong, and it needs a test pinning both directions before it can be trusted.

## 2.1.0 (2026-08-03)

(Numbering note: the SKILL.md `version` field moved to 2.0.0 with the SKILL + references split, which never got its own entry here. This entry follows that field, so 1.4.0 above is the last entry under the old numbering.)

One narrow exemption to the dash rule, plus the repo's first test suite. The no-dash rule went global on 2026-08-03, and it collided with the one shape that cannot comply: the harness's own memory-index entry, written as a markdown list item made of a link, a separator dash, and a one-line hook (`- [title](file.md) SEPARATOR hook text`). That format is specified by the harness, not by this skill, so every write of a compliant index file was being blocked with no way to fix the text. `greek_text_check.py` now exempts that line shape from the em/en-dash check only.

The exemption is deliberately hard to abuse. It requires a list bullet, a single markdown link with no spaces in the target, the separator, and a hook of at most 200 characters that contains no further dash of its own. A bullet of ordinary prose, a link with no bullet, a hook with a second dash, an empty or overlong hook, and any prose line whatsoever still block exactly as before, and every other rule (Oxford comma before «και», semicolon misuse, spacing, banned terms) still runs on the exempt line.

New `tests/test_index_line_exemption.py`, 14 cases, runnable under pytest or standalone. It pins both halves: an index line passes, and prose using the same character still fails. Verified additionally against a live memory index, which now scans clean.

## 1.4.0 (2026-07-16)

New Greek rule §18: **ordinals, not cardinals, for enumerated items in a series.** A post-nominal cardinal ("Ροή 2", "Κανόνας 3") reads as "Ροή δύο" and is an anglicism; Greek uses the ordinal ("Ροή 2η", "δεύτερη ροή"), the same pattern behind the weekday names Δευτέρα/Τρίτη/Τετάρτη/Πέμπτη. The carve-out is written into the rule: standardised citation and identifier numbers stay cardinal ("άρθρο 27", "παρ. 1", "ΦΕΚ Β΄ 235", "ν. 5144/2024", decision and version numbers), as does Arabic-numeral outline section numbering ("1. Θέμα"). Added a matching row to the Greek scan-patterns table. Deliberately NOT wired into the deterministic hook: a broad "noun + digit" regex would false-positive on the many legitimate cardinal citations, so §18 is a Pass-2 (native-reader) rule with Pass-1 scan guidance only. Prompted by a native-speaker correction and a live case (an RM memo that mixed "Ροή 1η" with "Ροή 2" / "Ροή 3").

## 1.3.1 (2026-06-30)

Hardened the `ENFORCE_ROOTS` comment against a real regression. A User-scope `HUMANIZED_TEXT_ENFORCE_ROOTS` env var had silently scoped enforcement to a few firm folders, so English deliverables in other projects bypassed the deterministic Pass-1 hook and shipped with em and en dashes. The env var has been removed (machine config), and the comment above `ENFORCE_ROOTS` now states the rule is universal and that no roots may be added: any value restricts the hook to matching paths and silently exempts everything else. Also genericised the documentation, removing firm-specific project names from CHANGELOG, SKILL.md and `references/greek_regulatory_terms.md` so the public skill carries no specific firm reference.

## 1.3.0 (2026-06-22)

Add `scripts/install_hook.sh`: an idempotent, one-command installer that symlinks `greek_text_check.py` into `~/.claude/scripts/` and merges the `PreToolUse(Write|Edit)` hook into `~/.claude/settings.json` (preserving every other key), then smoke-tests it. Motivated by a real miss: on a Linux machine the hook was documented but never wired, so the deterministic Pass-1 check never ran and em/en dashes shipped unblocked in English and Greek drafts. INSTALL.md now points at the installer as the default path. Also fixed an em dash in the INSTALL.md title (the repo must obey its own rule).

## 1.2.0 (2026-06-18)

New formatting rule, hook-enforced: **no space before punctuation**. `greek_text_check.py` now hard-blocks a space before `. , : ; ! ? · » …` and a space after the opening guillemet `«`. Documented in SKILL.md under Formatting Rules.

## 1.1.1 (2026-06-18)

Documentation: clarify that the `greek_text_check.py` hook scope is **universal** (every `.md`/`.txt` in any project that produces Greek, minus `EXEMPT_SEGMENTS`), not restricted to specific projects. No code change: `ENFORCE_ROOTS` already defaults to empty (universal); the prior "project-restricted" wording in `references/greek_regulatory_terms.md` was stale. Verified by a standalone scan on an unrelated-project path (em dash + «σκληρός φραγμός» both blocked, exit 2).

## 1.1.0 (2026-06-18)

Added the §16/§17 Greek terminology work from regulatory compliance sessions.

- §16: new Greek-to-Greek preferences with context nuance:
  - `σκληρός φραγμός` → `υποχρεωτικός αποκλεισμός` (calque of "hard stop"). `ανυπέρβλητο κώλυμα` and `συστημικός περιορισμός` remain valid in proper legal/technical context.
  - `απόλυτο κώλυμα` → `ρητή απαγόρευση`.
  - `ακόνισμα του σκεπτικού` → `εξειδίκευση της αιτιολογίας` (calque of "sharpen the reasoning").
  - `αγκύρωση / άγκυρα / αγκυρωμένος` (metaphorical) → `βάση / έρεισμα / θεμέλιο` (calque of "anchor/anchored").
- §17: EN↔EL legal glossary grounded in the **consolidated in-force** EUR-Lex texts: MiFID II (02014L0065-20260606), MiFIR (02014R0600-20251123), EMIR (02012R0648-20250117), DORA (Reg 2022/2554). Plus a SOP/eKYC/AML replacement table (`hard block` → `υποχρεωτικός περιορισμός` / `αυτόματη διακοπή λειτουργίας`).
- `scripts/greek_text_check.py`: `σκληρός φραγμός`, `σκληρό φραγμό`, `ακόνισμα του σκεπτικού`, `ακονίζω το σκεπτικό` added to `GREEK_HARD_BLOCK`. `απόλυτο κώλυμα` and `αγκύρωση` deliberately left out of the blocking hook (legitimate literal/legal uses) and kept as §16 prose guidance only.

## 1.0.0

Baseline: the pre-existing skill (banned phrases, structural patterns, formatting rules, full Greek grammar section §1-§16, `greek_text_check.py` PreToolUse hook, `references/greek_regulatory_terms.md`).
