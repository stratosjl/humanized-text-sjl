# humanized-text

A Claude Code skill that applies a natural human writing style to all generated prose, in English and Greek. The skill is a single Markdown file (`SKILL.md`) defining blocking pre-output checks: a list of banned phrases and AI catchphrases, a set of structural patterns to avoid (negative parallelism, rule-of-three abuse, elegant variation, copulative avoidance), formatting rules (no em dashes ever, no Title Case headings, no inline-header vertical lists, no curly quotes, no horizontal rules before headings), and a comprehensive Greek grammar section covering deponent verbs, genitive word order, acronym gender, definite articles with foreign names, word order with foreign modifiers, Oxford-comma in Greek, the middle dot versus the English semicolon, bilateral/multilateral terminology, clitic pronouns, Greek anglicisms in legal and financial writing, calques, common idiomatic errors, automated-check limits, and telegraphic phrases without conjugated verbs.

## Why this exists

Out of the box, an LLM writes the way the internet writes when the internet is being polite and trying to sound smart. That voice has tells: "stands as a testament to", "navigating the complexities of", "underscoring the importance of", excessive triplets, em dashes everywhere, copulative-avoidance, inline-header vertical lists. This skill is a counter-list. It tells the model what NOT to do, with specific replacements where the wrong thing is the easy default.

The Greek section is harder to find elsewhere. Greek-language LLM output frequently misuses deponent verbs as passives, drops definite articles before acronyms, places foreign modifiers before Greek head nouns, and substitutes the English semicolon for the middle dot. Each of those is a specific syntactic anglicism with a documented fix. Beyond the structural errors, the skill also covers legal and financial anglicisms (terms with good Greek equivalents that AI consistently leaves in English), calques (literal translations that read as translated rather than written), and telegraphic noun-plus-participle constructions ("Skill ενημερωμένο" instead of "Το Skill ενημερώθηκε"). The rules are stable Greek grammar; the examples in the tables are illustrative.

## Install

The skill is a single file. Drop it into your Claude Code skills directory:

```bash
# Linux / macOS
mkdir -p ~/.claude/skills/humanized-text
curl -fsSL https://raw.githubusercontent.com/stratosjl/humanized-text-sjl/main/SKILL.md \
  > ~/.claude/skills/humanized-text/SKILL.md
```

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills\humanized-text"
Invoke-WebRequest `
  https://raw.githubusercontent.com/stratosjl/humanized-text-sjl/main/SKILL.md `
  -OutFile "$env:USERPROFILE\.claude\skills\humanized-text\SKILL.md"
```

Or clone and symlink:

```bash
git clone https://github.com/stratosjl/humanized-text-sjl ~/Projects/humanized-text-sjl
ln -sfn ~/Projects/humanized-text-sjl ~/.claude/skills/humanized-text
```

The skill auto-loads at next Claude Code session start. Verify by typing `/help` and confirming `humanized-text` appears in the skills list.

## How to use

Once installed, the skill triggers automatically on every prose-generating request. The blocking PRE-OUTPUT VERIFICATION at the top of `SKILL.md` is what makes it work: Claude scans its draft against the banned-phrases and Greek-scan-patterns lists before emitting. There are no commands to run.

To test it: ask for a draft of anything in either language. Compare to a draft from a Claude session without the skill loaded.

## Source attribution

The "AI catchphrases and stock phrases" subsection was adapted from the [Wikipedia WikiProject AI Cleanup AI catchphrases](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup/AI_catchphrases) catalogue (CC BY-SA 4.0). The pattern list, structural-tells list, formatting-rules extensions, and citation-hygiene marker-token list draw on that page; the prose framing, plain-alternative replacements, Greek analogues, and structural-patterns section are this repo's own additions.

The Greek language section is original work, drawing on standard Greek grammar references (Τριανταφυλλίδης for the final-ν rule, the Νομική Υπηρεσία της Δημοκρατίας for bilateral/multilateral usage, and the linked Wikipedia and sch.gr articles for the middle dot). Each rule lists its sources inline.

## License

CC BY-SA 4.0. See [LICENSE](LICENSE).

The share-alike clause is mandatory: this work incorporates content adapted from Wikipedia (CC BY-SA 4.0), so derivatives must be released under a compatible license. Permissive-license forks (MIT/Apache) are not possible without removing or fully re-authoring the AI-catchphrases subsection.

## Contributing

Pull requests are welcome that:

- Catch new AI tells (catchphrases, structural patterns, formatting tics) with a citation if the source is a third-party catalogue like Wikipedia or a published style guide.
- Add Greek (or other-language) rules with worked examples and at least one published source.
- Tighten existing examples to be clearer or more general.

Pull requests are not welcome that:

- Add domain-specific examples (financial regulatory, medical, legal-jurisdiction-specific). The skill is intentionally general-purpose. Open a discussion if you think a domain extension belongs as a separate skill that builds on this one.
- Soften the no-em-dash rule. It is a hard rule for a reason: em dashes are the single most reliable LLM tell in English prose.
- Add ChatGPT or other model-specific patterns that do not also appear in Claude output. The skill is meant to be Claude-Code-installable but not Claude-specific.

Maintainership is light. PRs may take days to review.

## Provenance

This skill was originally extracted from a personal Claude Code configuration repo and first published as `humanized-text-skill` on 2026-05-08, after an audit confirming zero corporate, PII, MNPI, or client content. Earlier versions of the file used financial-regulatory examples (MiFID, GDPR, AIFMD); those were generalized to cross-domain examples (HTML, API, ISO, W3C, GDPR, AI Act) for the public release.

In the same session, a parallel development branch (`humanized-text`) was merged in. That branch extended the Greek grammar section from 10 rules to 15, adding coverage of legal/financial anglicisms (§11), calques (§12), common idiomatic errors (§13), the limits of automated checking (§14), and telegraphic noun-plus-participle constructions (§15). All financial-specific examples in those rules were generalized. The two repositories were merged into this one (`humanized-text-sjl`) under CC BY-SA 4.0.

The Greek grammar rules were unchanged by both the generalization pass and the merge; only the examples and framing were updated.
