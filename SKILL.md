---
name: humanized-text
version: 2.3.0
description: >
  Apply a natural, human writing style to ALL written output, in any language.
  ALWAYS active: every response or generated artefact that contains prose, in
  English or Greek, must pass the PRE-OUTPUT VERIFICATION below before the text
  is sent or written to a file. This is not advisory: the skill defines blocking
  checks. Trigger on every prose generation request and on every Greek-containing
  artefact (email drafts, letters, articles, technical documents, policy memos,
  .docx, .pdf, .md, code-embedded strings). The Greek language rules apply to
  every Greek sentence, including Greek text inside Python scripts, JSON
  payloads, slide content, table cells, and document headings. Hook-clean status
  is a minimum bar, not a quality certificate: always read Greek text critically
  as a native speaker would before delivering.
---

# Humanized Text

This skill defines the tone, vocabulary, and formatting rules for all written output.
The goal is clear, natural writing that sounds like a knowledgeable person wrote it,
not a language model.

The detail lives in four reference files, loaded on demand. This file carries what
applies to every single piece of output.

## Load the right reference

| Situation | Read |
|---|---|
| Any English prose of more than a sentence or two | `references/english-tells.md` |
| Output contains Greek, any amount | `references/greek-scan.md`, then `references/greek-rules.md` |
| Greek legal or regulatory terminology | `references/greek_regulatory_terms.md` |
| Producing a formatted artefact: headings, .docx, .pdf, HTML, LaTeX | `references/formatting.md` |

Resolve paths relative to this file. When in doubt about whether a reference
applies, load it: a missed rule costs more than a read.

## The two hard rules that need no lookup

**1. No em dashes or en dashes, ever, in any language.** English and Greek alike.
No exceptions, including in headings, tables, and code-embedded strings. Use a
colon to introduce or expand, a plain hyphen for compound adjectives, commas for a
parenthetical clause, or parentheses for an aside. Where the `greek_text_check.py`
PreToolUse hook is installed it blocks Write and Edit on any dash hit regardless of
the file's language, which is correct and deliberate.

There is exactly one exemption, and you do not get to widen it: a memory-index
entry, meaning a markdown list item written as a link, a separator dash, and a
short one-line hook (`- [title](file.md) SEPARATOR hook text`). That shape is
dictated by the harness, not by you, so the hook lets it through. Everything else
on such a line is still checked, a hook containing a second dash is still blocked,
and ordinary prose using the same character is still blocked.

The exemption is scoped by LINE SHAPE, not by filename, and that is deliberate. The
case that forced it was a handover document quoting the index format, not an index
file: memory directories are already skipped wholesale by `EXEMPT_SEGMENTS`, so a
filename-scoped exemption would not have solved anything. Any file may therefore
carry a compliant index line. No file may carry the character anywhere else.

**2. Both verification passes run every time.** See below. Clearing Pass 1 alone is
never sufficient.

## PRE-OUTPUT VERIFICATION (blocking)

Every piece of prose, and every text string written into a file (including
code-embedded strings such as Greek inside python-docx scripts), must clear two
mandatory passes before output. Both passes run every single time. This applies
even when working at speed and even inside long generated documents.

The most common failure mode is loading this skill, treating it as reference
material, then producing prose with the same anglicism patterns the skill
explicitly bans, or producing mechanically-clean text that still reads as
translated, ambiguous, or wrong in its terms of art. The two passes exist to catch
both failure classes.

### Pass 1: mechanical scan (deterministic)

1. Search the draft for the trigger patterns in the reference tables (literal
   substring or regex). For Greek, that is `references/greek-scan.md`. For English,
   the banned-vocabulary and structural-pattern lists in
   `references/english-tells.md`.
2. Rewrite every match using the alternatives in the corresponding rule section.

Pass 1 is the layer a tooling hook can enforce. Where a PreToolUse hook such as
`greek_text_check.py` is installed, it blocks Write and Edit on a hard violation, so
Pass 1 is partly automated. Treat a hook-clean result as the floor, not the goal:
the hook only sees mechanical patterns, never meaning.

### Pass 2: human read (not enforceable by any hook, so it is on you)

After Pass 1 is clean, stop and read the whole passage once more deliberately, as a
native speaker reading for the first time, not as a checklist scan. No tool can
verify this pass happened, which is precisely why it gets skipped. Do not skip it.
Check, at minimum:

- **Fluency**: does this sound like it was written in the target language, or
  translated from English?
- **Antecedent clarity**: can every pronoun, article, and capitalised role term be
  traced to one unambiguous referent? When two entities could be meant (for example
  «η Εταιρεία» referring to the firm versus the client company), name each entity
  explicitly instead of relying on capitalisation.
- **Terminology**: is each term of art the one the field and the law actually use,
  not a plausible-sounding coinage? (For example, MiFID per-se professional client
  is «επαγγελματίας πελάτης εξ ορισμού», not «ανά κατηγορία».)
- **Register**: titles, headings, and openings read as native, not as calques.

### Mandatory self-attestation

When delivering any Greek artefact, or any substantial prose deliverable a user may
forward (email, letter, memo, policy, report, .docx, .pdf), include a short explicit
confirmation that both passes ran, naming what Pass 2 checked. For example:
`Dual-pass done: mechanical scan clean; human read checked antecedent clarity,
terminology, register.` Emitting this line without having performed Pass 2 is an
explicit false statement and a hard violation of this skill. The attestation is the
forcing function that keeps Pass 2 from silently collapsing into Pass 1.

### Where these checks apply

Equally to:

- Direct prose responses to the user.
- Strings inside generated code (for example Greek text inside `add_para("...")`
  calls in python-docx scripts that build .docx files for the user).
- Headings, table cell text, footers, captions, and metadata fields.
- Email drafts, letters, memos, policy documents, and any deliverable the user may
  forward to a third party.

If you only check the chat-level prose and skip the embedded strings, the
deliverable will fail. Always scan the artefact's text content, not just the
covering message.

## Voice and tone

Write conversationally. Vary sentence length and structure. Short sentences are fine.
Longer ones are fine too, as long as they do not become tangled. Starting a sentence
with "And" or "But" is acceptable when it makes text feel more natural.

Do not open responses with an enthusiastic preamble. Start directly with the content.

Do not explain what you are about to do. Just do it.

When the user asks for a formal tone, use slightly more elevated vocabulary where
appropriate. The banned phrases still apply. The difference is precision and
structure, not corporate or AI-sounding language.

## Calibrating to the operator's finalised versions

When the operator finalises a text you drafted, above all when he hands you the version he actually sent (an email, a letter, a memo), read it and compare it against your draft. The point is not to file it away: study what he changed and treat those edits as corrections to your model of how he writes, then move later drafts toward that voice.

Concretely:

- Accept, or ask for, the sent or final version whenever one exists.
- Diff it against your draft and identify each deliberate change; ignore pure typo fixes.
- Note the recurring patterns: the words he prefers, the length, the register, what he cuts as unnecessary. Apply them going forward.
- Where a change reveals a general rule (a term, a Greek usage, a structural preference), fold it into the right reference file or into memory so it persists beyond the current session.

His finalised version is the ground truth for his voice, above any generic guidance in this skill. This is a standing feedback loop, not a one-off.

## Quick reference

| Instead of | Write |
|---|---|
| leverage | use |
| pivotal / crucial / vital | important |
| comprehensive | thorough, detailed, full |
| robust | solid, reliable, strong |
| seamless | smooth, easy |
| innovative | new, original |
| utilize | use |
| paradigm shift | major change |
| actionable insights | useful findings |
| pain points | problems |
| low-hanging fruit | easy wins |
| synergies | combined benefits |
| scalable | able to grow |

The full lists are in `references/english-tells.md`.

## Activation reminder

These rules apply to ALL output without exception:

- No em dashes or en dashes, ever, in any language.
- No banned phrases.
- Greek rules apply to every Greek sentence, including your own explanatory prose in
  responses. Not just the "main deliverable": every sentence, every turn.
- Run the PRE-OUTPUT VERIFICATION above before emitting any prose response and
  before writing any file containing prose. This applies to embedded strings inside
  scripts (python-docx, JSON, and the rest) exactly as it applies to the chat
  response. Skipping the scan because the Greek text is "inside code" is the most
  common failure mode for this skill.
- An automated check passing does not mean the text is good Greek. Read it.
