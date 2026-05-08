# humanized-text

A Claude Code skill that enforces clear, natural writing across all AI output. It blocks the filler phrases, AI jargon, and formatting habits that make generated text feel synthetic. For Greek-language output, it adds a second layer: grammar rules specific to mixed Greek-English professional writing, covering deponent verb misuse, word order anglicisms, and punctuation errors that automated checks miss.

---

## What it does

When you load this skill, Claude applies two overlapping sets of rules to every response before output.

**English (and language-agnostic) rules:**

- Bans assistant filler ("Absolutely!", "I'd be happy to help", "It's worth noting that...")
- Bans overused AI vocabulary (leverage, robust, seamless, pivotal, ecosystem, nuanced, holistic...)
- Bans corporate jargon (synergies, best practices, pain points, low-hanging fruit, stakeholders...)
- Bans clickbait hooks ("In today's digital age...", "Here's what nobody tells you...")
- Bans em dashes and en dashes in all output
- Bans template structure phrases ("Let's dive in", "Here are some key takeaways:")
- Enforces direct openings - no preamble, no explanation of what's about to happen

**Greek language rules (15 numbered rules):**

1. No em dashes in Greek text
2. Correct use of deponent verbs (διαχειρίζομαι, επεξεργάζομαι, διαπραγματεύομαι) - the single most common grammatical error in AI-generated Greek
3. Genitive word order: Greek head noun first, then the foreign modifier
4. Correct grammatical gender for acronyms and foreign terms (MiFID = η, GDPR = ο, DORA = ο)
5. Definite article required before acronyms and foreign brand names in subject/object position
6. Greek noun before foreign modifier in both category+identifier and compound-modifier patterns
7. No Oxford comma before "και"
8. Greek middle dot (·) instead of semicolon; the Greek semicolon is a question mark
9. Two-party agreements use διμερής, not αμφίπλευρος
10. Clitic pronoun required for known objects (το, την, τα, τον before the verb)
11. Greek equivalents for legal and financial anglicisms
12. No calques (literal translations of English collocations)
13. Common idiomatic errors ("Δίκιο σου" is wrong; "Έχεις δίκιο" is right)
14. Automated checks are a floor, not a ceiling - critical reading required
15. No telegraphic noun+participle constructions ("Skill ενημερωμένο" is wrong; "Το Skill ενημερώθηκε" is right)

The skill includes a PRE-OUTPUT VERIFICATION table: a blocking checklist of the highest-frequency errors with regex-style trigger patterns, likely errors, and exact fixes. Claude is expected to scan every prose response against this table before sending.

---

## Who this is for

Anyone who writes regularly with Claude and is bothered by the predictable patterns AI text tends to fall into. The English rules alone are useful. The Greek section is specifically for people who write professional Greek - regulatory documents, legal correspondence, financial reports - where AI-generated output often reads like translated English rather than natively written Greek.

The Greek rules were developed through real-world use in financial and regulatory contexts, where mistranslated grammar (especially deponent verb misuse and word order anglicisms) is both common and consequential.

---

## How to install

### As a Claude Code skill

Copy `SKILL.md` into your Claude skills directory:

**macOS / Linux:**
```bash
mkdir -p ~/.claude/skills/humanized-text
cp SKILL.md ~/.claude/skills/humanized-text/SKILL.md
```

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills\humanized-text"
Copy-Item SKILL.md "$env:USERPROFILE\.claude\skills\humanized-text\SKILL.md"
```

The skill is then available in Claude Code as `humanized-text`.

### Activation

The skill description marks itself as always-active:

```
ALWAYS active: every response or generated artefact that contains prose...
```

Claude Code will invoke it automatically at session start. You can also invoke it manually in any session with the Skill tool.

### Making it a permanent default

Add it to your global `CLAUDE.md`:

```markdown
Skills in use: humanized-text
```

Or reference it in a project-level `CLAUDE.md` to enable it only for specific projects.

---

## Customizing the Greek term list

The skill references a hard-block term list for Greek financial and regulatory writing. This list covers organization-specific terminology choices and grows over time. To maintain your own version:

1. Create a file at `~/.claude/skills/humanized-text/greek-term-overrides.md`
2. List any terms you want to add or override in the same table format as the skill
3. Reference this file in your `CLAUDE.md` as additional context

The core skill deliberately keeps only the terms that are unambiguously wrong in standard Greek. Industry-specific or organization-specific choices belong in your local override file.

---

## What it does NOT do

- It does not run a linter or automated text analysis tool. All enforcement happens in Claude's reasoning process.
- It does not translate between English and Greek.
- It does not rewrite your existing documents automatically - it shapes new output as Claude generates it.
- It does not cover every possible AI writing pattern. The listed rules address the most common failures; the approach is opinionated, not exhaustive.

---

## Structure

```
humanized-text/
├── SKILL.md          # The skill definition Claude loads
└── README.md         # This file
```

The skill is a single Markdown file. There are no dependencies, no scripts, no build steps.

---

## Background

The English rules emerged from frustration with Claude's default tendency to pad responses with affirmations, frame everything in corporate vocabulary, and open with structure announcements rather than content. The Greek rules emerged from a more specific problem: AI-generated Greek professional text consistently makes the same five or six grammatical errors that any native speaker notices immediately but that automated spell-checkers miss entirely.

Deponent verb misuse is the most frequent. A deponent verb like διαχειρίζομαι (to manage) has a passive-looking form but an active meaning. Its subject is always the agent. When AI generates "οι κεφαλαιαγορές διαχειρίζονται από την εταιρεία" (the capital markets are managed by the company), this is grammatically wrong - not just stylistically off. The correct form is "η εταιρεία διαχειρίζεται τις κεφαλαιαγορές" or "η διαχείριση των κεφαλαιαγορών ανήκει στην εταιρεία". The skill trains Claude to catch this class of error before it reaches the output.

---

## Contributing

The English rules are stable. Additions should meet a high bar: the phrase or pattern must be both common in AI output and clearly inferior to a natural alternative.

The Greek rules are more open to extension. If you work with Greek professional text and encounter patterns the skill misses, open an issue with:

- The error pattern (a trigger string or description)
- Why it is wrong (grammatical rule or reference)
- The correct alternative

Corrections to the regulatory reference table (§4, gender of acronyms) are especially welcome.

---

## License

MIT
