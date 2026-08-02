# English AI tells: banned vocabulary and structural patterns

Part of the `humanized-text` skill. Load this whenever generating English prose
of any length. Greek analogues are noted inline where they exist.

## Banned Phrases and Words

### Assistant filler phrases

Never use these:
- "Absolutely!", "Of course!", "Certainly!", "Great question!"
- "I'd be happy to help", "I'm here to help", "That's a fantastic point"
- "The short answer is...", "Let me break this down", "Here's the thing:"
- "In conclusion", "To sum up", "Ultimately"
- "It's worth noting that...", "It's important to note that..."
- "As a result", "In other words", "This means that..."
- "From a [X] perspective", "At the end of the day"
- "On the other hand"

### Overused AI vocabulary

Never use these:
- leverage, empowering, robust, seamless, intricate
- interplay, landscape, ecosystem, nuance/nuanced
- holistic, comprehensive, insightful, compelling, captivating
- engaging, thought-provoking, pivotal, paramount, crucial, vital
- innovative, cutting-edge, groundbreaking, paradigm shift, game-changing
- elevate, resonate, tapestry, dynamic, indelible, enigma, ethos

Use plain alternatives: "use" not "leverage", "important" not "pivotal",
"detailed" not "comprehensive".

### Clickbait and formulaic hooks

Never use these:
- "In today's digital age...", "In today's fast-paced world..."
- "Gone are the days when...", "Here's what nobody tells you..."
- "The secret sauce...", "Most people don't realize..."
- "This changes everything", "You won't believe..."
- "Mind-blowing fact:", "Fun fact:", "True story:", "The hard truth:"

### Corporate jargon

Never use these:
- synergies, best practices, pain points, low-hanging fruit
- value-driven, results-oriented, data-driven, actionable insights
- scalable, optimize/optimization (as buzzwords)
- alignment/misalignment (buzzword sense), strategic roadmap
- stakeholders, industry-leading, world-class, cutting-edge solutions

### Template-like structure phrases

Never use these:
- "Let's explore...", "Let's dive in", "We'll cover the following:"
- "Here are some key takeaways:", "Here's a breakdown:"
- "On the flip side", "By following these steps"

Avoid rigid sequences like "First, second, third, finally" unless the user
explicitly asks for a step-by-step format.

### AI catchphrases and stock phrases

Source: Wikipedia WikiProject AI Cleanup pattern catalogue. These are the
highest-frequency tells editors flag when they suspect a draft is
machine-generated. Most apply to English text; several have direct Greek
analogues (noted inline).

Significance, legacy, and trends:
- "stands as / serves as a testament", "is a testament to"
- "underscores / highlights its importance"
- "reflects broader [trends / themes]"
- "symbolizes its ongoing / enduring / lasting"
- "contributing to the [field / discourse / understanding]"
- "setting the stage for"
- "marking / shaping the [era / period]"
- "represents a shift", "marks a shift"
- "key turning point", "watershed moment"
- "evolving landscape", "focal point"
- "indelible mark", "deeply rooted"

Greek analogue: «αποτελεί ορόσημο», «σηματοδοτεί νέα εποχή»,
«διαμορφώνει το τοπίο» land as the same kind of grandstanding. Use only
when a specific, concrete claim about scale or consequence is being made.

Promotional and travel-brochure language:
- "boasts a", "boasts" as a verb
- "rich [history / heritage / tradition]"
- "profound" outside specifically philosophical contexts
- "showcasing", "exemplifies"
- "commitment to [excellence / quality]"
- "natural beauty", "nestled", "in the heart of"
- "renowned", "featuring", "diverse array"

Vague attribution:
- "Industry reports", "Observers have cited"
- "Experts argue", "Some critics argue"
- "Several sources / publications [say / report]"
- "Such as" introducing a long, exhaustive list (just give the list, or
  use "including" sparingly)

Section and structural formulae:
- "Despite its ..., faces several challenges"
- "Despite these challenges, ..."
- "Challenges and Legacy" as a heading
- "Future Outlook" as a heading

Greek analogue: «Παρά τις προκλήσεις...», «Μελλοντικές προοπτικές» as a
default closing section reads as the same template tic.

### Additional overused AI vocabulary (extends the list above)

Not already in the main banned-vocabulary block:

| Avoid | Plain alternative |
|---|---|
| Additionally (sentence opener) | also, and |
| align with | match, fit |
| boasts | has |
| bolstered | strengthened, helped |
| delve into | look at, examine, study |
| emphasizing | stressing |
| enduring | lasting |
| enhance | improve |
| fostering | growing, helping |
| garner | earn, get, attract |
| highlight (as a verb) | point out, show, mark |
| key (as an adjective) | most important, main |
| meticulous, meticulously | careful, carefully, exact |
| showcase | show, present |
| testament | proof, sign |
| underscore (as a verb) | stress, point out |
| valuable | useful |
| vibrant | lively |

The "use plain alternatives" principle applies even when the formal register
of the document allows precise technical vocabulary. "Important" beats
"crucial" beats "pivotal" in almost every context that is not specifically
literary.

---

## Structural patterns to avoid

These are sentence-level and paragraph-level patterns that mark text as
machine-generated even when individual words are unobjectionable. They
appear in English and Greek output alike.

### Negative parallelism

Never write:
- "Not just X, but also Y"
- "Not X, but Y" (as a stylistic flourish, not when literally needed)
- "It is not ..., it's ..."
- "No ..., no ..., just ..."

The construction is fine once. Used twice in the same piece, it lands as a
tic. Greek analogue: «Όχι απλώς X, αλλά και Y» suffers the same fate.
Pick a positive statement instead.

### Rule-of-three abuse

Avoid stacking three adjectives, three short phrases, or three "X, Y, and Z"
clauses in close succession. A triplet that fits a specific sentence is
fine. A triplet in every paragraph is a tell. Vary sentence length and
rhythm; do not let "A, B, and C" become a default.

### Elegant variation

Do not cycle through synonyms to avoid repeating a word. If "company" is
the right word, write "company" three times. Do not switch to "firm",
"organization", "entity" merely for variety. Repetition is honest;
synonym-cycling is mannered. The same applies to Greek: «η εταιρεία» three
times beats «η εταιρεία», «ο όμιλος», «ο φορέας» when the referent is one
specific company.

### Avoidance of copulatives

Do not substitute the plain copulas "is", "are", "has", or "have" with
stand-ins like:
- serves as / stands as / marks / represents (in place of "is")
- features / offers / maintains / boasts (in place of "has")
- "X refers to ..." as a lead sentence

Plain copulas are the right default. Stand-ins are appropriate only when
they carry distinct meaning the copula does not. Greek analogue: do not
default to «λειτουργεί ως», «αποτελεί», «συνιστά» when «είναι» is correct.

### Reference and citation hygiene (when generating prose with citations)

If the deliverable carries citations:
- Verify external links resolve before listing them.
- Do not invent DOIs, ISBNs, or page numbers.
- Strip `utm_source` and other tracking parameters from URLs.
- Do not declare named references that the article body never uses.
- Do not produce broken markup (mismatched brackets, half-closed tags).
- Watch for marker tokens that leak from upstream tooling (`turn0search0`,
  `oaicite`, `oai_citation`, `contentReference`, `attached_file`,
  `grok_card`, `attribution`, `attributableIndex`). If any appear in the
  draft, strip them before output.
