# Changelog

## 1.2.0 (2026-06-18)

New formatting rule, hook-enforced: **no space before punctuation**. `greek_text_check.py` now hard-blocks a space before `. , : ; ! ? · » …` and a space after the opening guillemet `«`. Documented in SKILL.md under Formatting Rules.

## 1.1.1 (2026-06-18)

Documentation: clarify that the `greek_text_check.py` hook scope is **universal** (every `.md`/`.txt` in any project that produces Greek, minus `EXEMPT_SEGMENTS`), not restricted to HAM/Vigor. No code change: `ENFORCE_ROOTS` already defaults to empty (universal); the prior "Vigor-only" wording in `references/greek_regulatory_terms.md` was stale. Verified by a standalone scan on a non-Vigor path (em dash + «σκληρός φραγμός» both blocked, exit 2).

## 1.1.0 (2026-06-18)

Added the §16/§17 Greek terminology work from the HAM regulatory sessions.

- §16: new Greek-to-Greek preferences with context nuance:
  - `σκληρός φραγμός` → `υποχρεωτικός αποκλεισμός` (calque of "hard stop"). `ανυπέρβλητο κώλυμα` and `συστημικός περιορισμός` remain valid in proper legal/technical context.
  - `απόλυτο κώλυμα` → `ρητή απαγόρευση`.
  - `ακόνισμα του σκεπτικού` → `εξειδίκευση της αιτιολογίας` (calque of "sharpen the reasoning").
  - `αγκύρωση / άγκυρα / αγκυρωμένος` (metaphorical) → `βάση / έρεισμα / θεμέλιο` (calque of "anchor/anchored").
- §17: EN↔EL legal glossary grounded in the **consolidated in-force** EUR-Lex texts: MiFID II (02014L0065-20260606), MiFIR (02014R0600-20251123), EMIR (02012R0648-20250117), DORA (Reg 2022/2554). Plus a SOP/eKYC/AML replacement table (`hard block` → `υποχρεωτικός περιορισμός` / `αυτόματη διακοπή λειτουργίας`).
- `scripts/greek_text_check.py`: `σκληρός φραγμός`, `σκληρό φραγμό`, `ακόνισμα του σκεπτικού`, `ακονίζω το σκεπτικό` added to `GREEK_HARD_BLOCK`. `απόλυτο κώλυμα` and `αγκύρωση` deliberately left out of the blocking hook (legitimate literal/legal uses) and kept as §16 prose guidance only.

## 1.0.0

Baseline: the pre-existing skill (banned phrases, structural patterns, formatting rules, full Greek grammar section §1-§16, `greek_text_check.py` PreToolUse hook, `references/greek_regulatory_terms.md`).
