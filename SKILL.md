---
name: humanized-text
description: >
  Apply a natural, human writing style to ALL written output, in any language.
  ALWAYS active: every response or generated artefact that contains prose, in
  English or Greek, must pass the PRE-OUTPUT VERIFICATION at the top of this
  file BEFORE the text is sent or written to a file. This is not advisory: the
  skill defines blocking checks. Trigger on every prose generation request and
  on every Greek-containing artefact (email drafts, letters, regulatory text,
  policy memos, .docx, .pdf, .md, code-embedded strings, AND every direct
  response to the user in the console that contains Greek text). The Greek
  language rules apply to every Greek sentence, including Greek text inside
  Python scripts, JSON payloads, slide content, table cells, and document
  headings. Hook-clean status is a minimum bar, not a quality certificate:
  always read Greek text critically as a native speaker would before delivering.
---

# Humanized Text

This skill defines the tone, vocabulary, and formatting rules for all written output.
The goal is clear, natural writing that sounds like a knowledgeable person wrote it,
not a language model.

---

## PRE-OUTPUT VERIFICATION (blocking)

**Before sending any response that contains prose, and before writing any text into
a file (including code-embedded strings such as Greek inside python-docx scripts),
mentally scan the draft against the checklist below. Any match must be rewritten
before output. This applies even when working at speed and even inside long
generated documents.**

**This check applies equally to console responses and to file content. There is no
exemption for "short answers", "quick clarifications", or "inline explanations".**

The most common failure mode is loading this skill, treating it as reference
material, then producing Greek prose with the same anglicism patterns the skill
explicitly bans. To prevent that:

1. After drafting Greek prose, read it back with the checklist in mind.
2. Search for the trigger patterns below (literal substring or regex).
3. Rewrite every match using the alternatives in the corresponding rule section.
4. Then read the whole passage once more as a native speaker, not as a checklist
   scan but as a fluency check. Ask: does this sound like it was written in Greek,
   or translated from English?

### Greek scan patterns (highest-frequency errors)

| Trigger pattern in the draft | Likely error | Fix |
|---|---|---|
| Deponent verb form `…ίζονται από` / `…εύονται από` / `…ούνται από` | Deponent abused as true passive (Rule §2 below) | Use nominalisation (`τη διαχείριση έχει αναλάβει η Χ`, `γίνεται διαπραγμάτευση`) or true passive (`υποβάλλεται`, `εξετάζεται`) |
| `διαχειρίζονται από` | The single most common error in financial/maritime Greek | `υπό τη διαχείριση της Χ` / `τη διαχείρισή τους έχει αναλάβει η Χ` |
| `επεξεργάζονται από` | Same | `υπόκεινται σε επεξεργασία από` / `τα επεξεργάζεται η Χ` |
| `διαπραγματεύονται από` | Same | `αποτελούν αντικείμενο διαπραγμάτευσης από` |
| `ασχολούνται από` | Same | `εξετάζονται από` / `αντιμετωπίζονται από` |
| Ακρωνύμιο ακολουθούμενο από ελληνικό ουσιαστικό χωρίς άρθρο (π.χ. `MiFIR αναφορά`) | Αγγλική σειρά λέξεων (Κανόνας §3) | Το ελληνικό ουσιαστικό πρώτα: `αναφορά κατά τον MiFIR` |
| Ακρωνύμιο ως γραμματικό υποκείμενο χωρίς άρθρο (`GDPR προβλέπει`) | Απόντα οριστικό άρθρο (Κανόνας §5) | `ο GDPR προβλέπει`, `η MiFID απαιτεί` |
| Ξένο ουσιαστικό πριν το ελληνικό (`MiFIR transaction reporting`) | Ξένος τροποποιητής σε θέση κεφαλής (Κανόνας §6) | Ελληνικό ουσιαστικό πρώτα: `αναφορά συναλλαγών κατά τον MiFIR` |
| Ξένος σύνθετος τροποποιητής πριν το ελληνικό ουσιαστικό (`real-time επεξεργασία`) | Ίδια οικογένεια (Κανόνας §6 Πρότυπο Β) | Ελληνικό ουσιαστικό πρώτα: `επεξεργασία real-time` |
| Ξένη επωνυμία χωρίς άρθρο (`από Chase`, `μέσω UBS`) | Απόντα οριστικό άρθρο (Κανόνας §5) | `από την Chase`, `μέσω της UBS` |
| `, και` οπουδήποτε σε ελληνικό κείμενο | Αγγλικισμός (Oxford comma, απαγορεύεται από τον Κανόνα §7) | Αφαίρεσε το κόμμα: `, και` → ` και` |
| `;` μέσα σε πρόταση ακολουθούμενο από πεζό ελληνικό γράμμα | Αγγλικό semicolon σε ελληνικό κείμενο (Κανόνας §8) | Αντικατάστησε με `·` (U+0387), χωρίς κενό πριν |
| `αμφίπλευρ*` για σχέσεις ή συμφωνίες δύο μερών | Λάθος λέξη για "bilateral" (Κανόνας §9) | Αντικατάστησε με `διμερ*` (διμερής, διμερή, διμερείς) |
| Αγγλικός χρηματοοικονομικός ή νομικός όρος ως ουσιαστικό στο ελληνικό κείμενο | Αγγλικισμός (Κανόνας §11) | Χρησιμοποίησε ελληνικό ισοδύναμο από τον πίνακα §11 |
| Κατά λέξη μετάφραση αγγλικής έκφρασης (π.χ. `στατιστικά λεπτό δείγμα`) | Calque (Κανόνας §12) | Ξανάγραψε σε φυσικά ελληνικά |
| `δίκιο σου` ως αυτόνομη επιβεβαίωση | Λάθος ελληνικό ιδίωμα (Κανόνας §13) | `Έχεις δίκιο` |
| `αξιολόγηση ορθότητας` σε MiFID/ρυθμιστικό πλαίσιο | Λάθος MiFID II όρος | `αξιολόγηση συμβατότητας` (Άρθρο 25 παρ. 3 Ν. 4514/2018) |
| Ελληνικό ουσιαστικό ή άρθρο + ελληνική μετοχή/επίθετο χωρίς συνδετικό ρήμα (`Skill ενημερωμένο`) | Τηλεγραφικός αγγλικισμός, ύφος "X updated" (Κανόνας §15) | Πλήρης ελληνική πρόταση: `Το Skill ενημερώθηκε` |

### Hard-block terms reference

The following English terms commonly appear in Greek professional prose but should be
replaced with their Greek equivalents. Extend this list with your own industry-specific
overrides in a local file.

Key substitutions:

| English | Greek |
|---|---|
| canonical | εγκυρότερη / αναφορική / επίσημη |
| bilateral | διμερής |
| multilateral | πολυμερής |
| unilateral | μονομερής |
| consent | συναίνεση |
| attestation | βεβαίωση |
| Conditions Precedent | Προαπαιτούμενα |
| escalation | κλιμάκωση |
| scope | πεδίο / εύρος |
| trigger | ενεργοποίηση |
| carve-out / carveout | εξαίρεση |
| artifacts / artifact | κείμενα / κείμενο |
| warranty | εγγύηση |
| softened / softer | μαλακότερο / ηπιότερο |
| tighten | αυστηροποίηση |
| rollback | επαναφορά |
| fallback | εφεδρική επιλογή |
| covenant | ρήτρα |
| redline | παρατήρηση επί του κειμένου |

Technical MiFID-anchored terms that may remain English: audit trail, letterbox,
retrocession, outsourcing, best execution, due diligence, compliance, threshold,
tipping-off, thematic review, investment advice, QET, TCA.

### Scope reminder

These checks apply equally to:
- Direct prose responses to the user in the console (every sentence, every turn).
- Strings inside generated code (e.g. Greek text inside `add_para("...")` calls in
  python-docx scripts that build .docx files for the user).
- Headings, table cell text, footers, captions, and metadata fields.
- Email drafts, letters, regulatory memos, policy documents, and any deliverable
  the user may forward to a third party.

If you only check the chat-level prose and skip the embedded strings, the
deliverable will fail. Always scan the artefact's text content, not just the
covering message.

---

## Voice and Tone

Write conversationally. Vary sentence length and structure. Short sentences are fine.
Longer ones are fine too, as long as they do not become tangled. Starting a sentence
with "And" or "But" is acceptable when it makes text feel more natural.

Do not open responses with an enthusiastic preamble. Start directly with the content.

Do not explain what you are about to do. Just do it.

---

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

---

## Formatting Rules

**No em dashes or en dashes, ever.** This is a hard rule with no exceptions.
Use one of these instead, depending on context:
- a colon (:) to introduce or expand
- a plain hyphen (-) for compound adjectives
- commas to enclose a parenthetical clause
- parentheses () for asides

Do not use unnecessary quotation marks around ordinary words.

Do not over-format with heavy headings and bullet lists unless the user asks for a
structured outline.

Do not repeat the same opening sentence structure across responses.

---

## When the User Asks for Formal Tone

Use slightly more elevated vocabulary where appropriate. The banned phrases above
still apply. The difference is precision and structure, not corporate or AI-sounding
language.

---

## Quick Reference

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

---

## Greek Language Rules

Apply these rules whenever output contains Greek text, including mixed Greek-English
documents (regulatory, HR, legal, internal memos). These rules apply equally to
console responses and to file content: there is no context where they are suspended.

### 1. No em dashes in Greek text

Same rule as above. Replace the em dash with ":", "-", commas, or parentheses. The
em dash is not a natural punctuation mark in Greek prose.

### 2. Deponent verbs (Αποθετικά ρήματα)

Deponent verbs have a passive/middle form (-μαι) but carry active meaning. The
subject is always the agent, never the recipient of the action. Do NOT use them to
express a true passive.

Common deponents in formal/regulatory writing:

| Verb | Meaning | Wrong (passive misuse) | Right |
|------|---------|------------------------|-------|
| επεξεργάζομαι | I process | τα δεδομένα θα επεξεργαστούν | θα γίνει επεξεργασία των δεδομένων / θα υποστούν επεξεργασία |
| διαπραγματεύομαι | I negotiate | οι όροι θα διαπραγματευτούν | θα γίνει διαπραγμάτευση των όρων |
| απευθύνομαι | I address | η αίτηση θα απευθυνθεί | η αίτηση θα υποβληθεί |
| αναφέρομαι | I refer | θα αναφερθεί στο έγγραφο | γίνεται αναφορά στο έγγραφο |
| ασχολούμαι | I deal with | το θέμα θα ασχοληθεί | το θέμα θα εξεταστεί |
| δέχομαι | I accept | η πρόταση δε θα δεχθεί | η πρόταση δεν θα γίνει αποδεκτή |
| σκέπτομαι | I consider | η λύση σκέφτηκε | η λύση εξετάστηκε |
| προσφεύγομαι | I resort to | η διαδικασία θα προσφύγει | θα γίνει προσφυγή σε |

**Rule:** If the grammatical subject is NOT the agent performing the action,
restructure using:
- Nominalisation: "θα γίνει + noun" (θα γίνει επεξεργασία)
- True passive verb: "θα υποστεί", "θα εξεταστεί", "θα υποβληθεί"
- Introduce an explicit agent: "Η εταιρεία θα επεξεργαστεί τα δεδομένα"

Quick check: search draft for verb forms ending in -στούν, -στεί, -στούμε,
-ζόταν. If the subject is not the doer, rewrite.

### 3. Genitive (possessive) word order

Greek uses the possessive genitive: "το X του/της/των Y", not "Y X". Placing a
noun before another noun as a modifier (English compounding) is a syntactic
anglicism and is wrong in Greek.

| Wrong (anglicism) | Right |
|---|---|
| MiFIR προβλέψεις | προβλέψεις της MiFIR |
| GDPR απαιτήσεις | απαιτήσεις του GDPR |
| risk manager αρμοδιότητες | αρμοδιότητες του risk manager |
| σύμφωνα με DORA διατάξεις | σύμφωνα με τις διατάξεις της DORA |

The pattern is always: head noun first, then genitive of the modifier.

### 4. Gender of pronouns and articles for acronyms and foreign terms

When a Greek article or pronoun is needed for an acronym or foreign term, determine
the gender by translating the underlying noun to Greek and using that noun's gender.

Step-by-step process:
1. What is the acronym/term? (e.g., MiFID, GDPR, DORA, AIF, AIFMD)
2. What does it stand for in English? (e.g., Directive, Regulation, Act, Fund)
3. What is the Greek translation of that noun?
4. What gender is the Greek noun?
5. Use that gender for all articles and pronouns referring to it.

Reference table for common regulatory terms:

| Term | Full name | Greek noun | Gender | Use |
|------|-----------|------------|--------|-----|
| MiFID | Directive | Οδηγία | θηλυκό | η MiFID, της MiFID |
| MiFIR | Regulation | Κανονισμός | αρσενικό | ο MiFIR, του MiFIR |
| GDPR | Regulation | Κανονισμός | αρσενικό | ο GDPR, του GDPR |
| DORA | Regulation (Act) | Κανονισμός | αρσενικό | ο DORA, του DORA |
| AIFMD | Directive | Οδηγία | θηλυκό | η AIFMD, της AIFMD |
| SFDR | Regulation | Κανονισμός | αρσενικό | ο SFDR, του SFDR |
| PRIIPs | Regulation | Κανονισμός | αρσενικό | ο PRIIPs, του PRIIPs |
| EMIR | Regulation | Κανονισμός | αρσενικό | ο EMIR, του EMIR |
| AIF | Fund | Αμοιβαίο Κεφάλαιο / Ταμείο | ουδέτερο | το AIF, του AIF |
| MiCA | Regulation | Κανονισμός | αρσενικό | ο MiCA, του MiCA |
| NIS2 | Directive | Οδηγία | θηλυκό | η NIS2, της NIS2 |
| AI Act | Regulation | Κανονισμός | αρσενικό | ο AI Act, του AI Act |

### 5. Definite article with acronyms and foreign names

Greek requires a definite article before acronyms, abbreviations, and foreign brand
names when they are grammatical subjects or objects. Do not drop the article.

| Wrong | Right |
|---|---|
| GDPR προβλέπει | ο GDPR προβλέπει |
| MiFID απαιτεί | η MiFID απαιτεί |
| DORA εισάγει υποχρεώσεις | ο DORA εισάγει υποχρεώσεις |
| Σύμφωνα με AIFMD | Σύμφωνα με την AIFMD |

Exception: after a preposition that forms a compound with the article (e.g., "κατά
τον GDPR", "βάσει της MiFID"), the article is present but fused with the preposition.

### 6. Word order: Greek noun before foreign modifier (παράθεση)

This rule covers two related patterns, both with the same root cause.

**Pattern A - Category + technical identifier:**
When naming a technical object, place the Greek category noun first, then the
foreign identifier as apposition.

| Wrong | Right |
|---|---|
| το 'humanized-text' skill | το skill 'humanized-text' |
| η 'user_id' μεταβλητή | η μεταβλητή 'user_id' |
| ο 'Orders' πίνακας | ο πίνακας 'Orders' |

**Pattern B - Greek noun + foreign compound modifier:**
When a foreign compound (e.g., "cross-session", "real-time", "back-office") acts as
a modifier of a Greek noun, the Greek noun comes first, the foreign modifier follows.

| Wrong | Right |
|---|---|
| cross-session ανάκληση | ανάκληση cross-session |
| real-time επεξεργασία | επεξεργασία real-time |
| back-office διαδικασίες | διαδικασίες back-office |
| end-to-end κρυπτογράφηση | κρυπτογράφηση end-to-end |

Both patterns have the same root cause: in Greek, the article must connect directly
to the head noun (the category/Greek word) to signal gender and case. A foreign,
uninflected term cannot carry this function. Placing it before the head noun creates
a syntactic gap and is a syntactic anglicism that sounds wrong to any native speaker.

The analogy from Classical Greek: "ο βασιλιάς Κύρος", never "ο Κύρος βασιλιάς".
This pattern has been stable in Greek for 2,500 years.

**This rule applies to Claude's own prose in responses, not only to content
generated for the user.** Any Greek sentence in any response must follow it.

### 7. Κόμμα πριν το «και»

Στα ελληνικά **δεν προηγείται κόμμα** του «και» όταν αυτό συνδέει δύο όρους ή δύο προτάσεις σε απλή σύνδεση. Το πρότυπο `, και` είναι αγγλικισμός (Oxford comma).

Παραδείγματα:

- Λάθος: Διαβάζω, και γράφω. / Σωστό: Διαβάζω και γράφω.
- Λάθος: Έγραψε την επιστολή, και την υπέγραψε. / Σωστό: Έγραψε την επιστολή και την υπέγραψε.

**Εξαιρέσεις (όπου το κόμμα είναι σωστό):**

1. Όταν το «και» έπεται παρενθετικής φράσης που οριοθετείται με κόμματα: «Ο Γιάννης, που είναι αδερφός μου, και η Μαρία ήρθαν.» Εδώ το κόμμα ανήκει στην παρενθετική, όχι στο «και».
2. Όταν το «και» εισάγει εντελώς νέα σκέψη ή αντίθεση: «Είπε όχι, και είχε δίκιο.»

**Κανόνας:** Σε αμφιβολία, αφαίρεσε το κόμμα.

### 8. Άνω τελεία (·) αντί αγγλικού semicolon

Όπου στα αγγλικά μπαίνει `;` (semicolon), στα ελληνικά μπαίνει **άνω τελεία** (`·`, U+0387). Το ελληνικό `;` είναι το ερωτηματικό, όχι semicolon.

**Πότε χρησιμοποιείται η άνω τελεία:**

1. Διαχωρίζει δύο κύριες προτάσεις με στενό νοηματικό σύνδεσμο, όπου η δεύτερη επεξηγεί ή αντιπαραθέτει την πρώτη.
2. Προ-εισάγει εξήγηση ή συνέπεια χωρίς να σταματά τη ροή.
3. Διαχωρίζει στοιχεία λίστας όταν τα ίδια τα στοιχεία περιέχουν κόμματα.

**Στίξη:** δεν προηγείται κενό· ακολουθεί κενό· η επόμενη λέξη γράφεται με **πεζό** αρχικό γράμμα. Η παύση είναι ισχυρότερη του κόμματος και ελαφρύτερη της τελείας.

Παραδείγματα:
- Λάθος: Έγραψα την έκθεση; δεν την έστειλα ακόμα.
- Σωστό: Έγραψα την έκθεση· δεν την έστειλα ακόμα.

### 9. Διμερής / Πολυμερής / Μονομερής

Στα ελληνικά:

| Αγγλικά | Σωστά ελληνικά | Παράδειγμα |
|---|---|---|
| bilateral | διμερής | διμερής συμφωνία, διμερείς σχέσεις |
| multilateral | πολυμερής | πολυμερής σύμβαση |
| unilateral | μονομερής | μονομερής δήλωση |

**Όχι «αμφίπλευρος».** Το επίθετο «αμφίπλευρος» στα ελληνικά αναφέρεται σε κάτι που **έχει δύο πλευρές** (π.χ. αμφίπλευρη παράλυση, αμφίπλευρο σχέδιο), όχι σε σχέση μεταξύ δύο μερών.

| Λάθος | Σωστό |
|---|---|
| αμφίπλευρα κείμενα | διμερή κείμενα |
| αμφίπλευρη συμφωνία | διμερής συμφωνία |
| αμφίπλευρες σχέσεις | διμερείς σχέσεις |

### 10. Κλιτική αντωνυμία (clitic pronoun) για γνωστό αντικείμενο

Όταν ένα μεταβατικό ρήμα αναφέρεται σε αντικείμενο που έχει ήδη αναφερθεί ή είναι κατανοητό από τα συμφραζόμενα, η ελληνική απαιτεί τον αδύνατο τύπο της αντωνυμίας (το, την, τα, τον κ.λπ.) πριν από το ρήμα.

| Λάθος | Σωστό |
|---|---|
| διαχειρίζεσαι εσύ (αναφορά σε φάκελο) | το διαχειρίζεσαι εσύ |
| διαχειρίζεται το Claude app | το διαχειρίζεται το Claude app |
| επεξεργάζεται η εταιρεία | το επεξεργάζεται η εταιρεία |
| αναφέρει το έγγραφο | το αναφέρει το έγγραφο |

Ο κανόνας: αν το αντικείμενο είναι γνωστό από τα προηγούμενα, βάλε πάντα τον αδύνατο τύπο (το/την/τα/τον) πριν το ρήμα.

### 11. Αγγλισμοί στο νομικό και χρηματοοικονομικό λεξιλόγιο

Πολλοί αγγλικοί νομικοί και χρηματοοικονομικοί όροι έχουν φυσικά ελληνικά ισοδύναμα και πρέπει να αντικαθίστανται στο ελληνικό πεζό κείμενο, ακόμα και όταν ο αυτοματοποιημένος έλεγχος δεν τους εντοπίσει.

**Κανόνας:** Αν ένας αγγλικός όρος δεν είναι αγκυρωμένος σε συγκεκριμένη ευρωπαϊκή νομοθεσία ως τεχνικός ορισμός (MiFID, DORA, EBA κ.λπ.), χρησιμοποίησε το ελληνικό ισοδύναμο.

| Αγγλικό (αποφεύγεται στο πεζό κείμενο) | Ελληνικό ισοδύναμο |
|---|---|
| substance KPIs | δείκτες ουσίας |
| capacity assessment | αξιολόγηση λειτουργικής επάρκειας |
| Compliance Officers | Υπεύθυνοι Κανονιστικής Συμμόρφωσης |
| suitability assessment (σε πεζό κείμενο) | αξιολόγηση καταλληλότητας |
| appropriateness assessment | αξιολόγηση συμβατότητας |
| governance gate | μηχανισμός εγκρίσεων διακυβέρνησης |
| onboarding | ένταξη πελατών |
| reporting | υποβολή αναφορών / αναφορά |
| monitoring | παρακολούθηση / εποπτεία |
| softened / softer | μαλακότερο / ηπιότερο |
| tighten | αυστηροποίηση |
| rollback | επαναφορά |
| fallback | εφεδρική επιλογή |
| covenant | ρήτρα |
| redline | παρατήρηση επί του κειμένου |

**Τεχνικοί όροι που παραμένουν αγγλικά** (λόγω MiFID/DORA/EBA άγκυρας): audit trail, letterbox, retrocession, outsourcing, best execution, due diligence, compliance (ως τμήμα), threshold, tipping-off, thematic review, investment advice, QET, TCA.

### 12. Calques — μη μεταφράζεις αγγλικές εκφράσεις κατά λέξη

Ένας calque είναι η λεξιλογική δανεική μετάφραση αγγλικής έκφρασης που ακούγεται ξένη στα ελληνικά. Τεχνικά ορθή φράση μπορεί να είναι φυσικά αδόκιμη.

**Κανόνας ύφους για επίσημα/νομικά κείμενα:** Αποφεύγω δραματικά ή μεταφορικά ρήματα ακόμα και αν είναι τεχνικά ορθά ελληνικά. Στο επίσημο κείμενο, το ουδέτερο ισοδύναμο είναι πάντα η καλύτερη επιλογή.

| Αγγλική έκφραση | Calque (λάθος) | Φυσικά ελληνικά |
|---|---|---|
| statistically thin sample | στατιστικά λεπτό δείγμα | δείγμα ανεπαρκούς μεγέθους · ο όγκος των δεδομένων είναι πολύ μικρός για αξιόπιστο συμπέρασμα |
| at the end of the day | στο τέλος της ημέρας | τελικά · εν τέλει |
| red flag | κόκκινη σημαία | ανησυχητικό σήμα · προειδοποιητικό σημάδι |
| window of opportunity | παράθυρο ευκαιρίας | ευκαιρία · κατάλληλη συγκυρία |
| moving forward | προχωρώντας μπροστά | στη συνέχεια · από εδώ και πέρα |
| track record | αρχείο επιδόσεων | ιστορικό · αποδεδειγμένη εμπειρία |
| due diligence (ως ρήμα) | κάνω due diligence | διενεργώ έλεγχο due diligence |

**Δοκιμή:** Διάβασε τη φράση σε έναν φυσικό ομιλητή. Αν χαμογελάσει ή απορεί, είναι calque.

### 13. Κοινά ιδιωματικά λάθη

Συγκεκριμένες εκφράσεις που συχνά παράγονται λανθασμένα:

| Λάθος | Σωστό | Σημείωση |
|---|---|---|
| Δίκιο σου. | Έχεις δίκιο. | «Δίκιο σου» δεν είναι φυσική ελληνική φράση ως αυτόνομη επιβεβαίωση. |
| Συγχαρητήρια για την ερώτηση. | (αποφεύγεται εντελώς) | Τυπικός αγγλισμός (Great question!). |
| Να είσαι σίγουρος ότι... | Να είσαι βέβαιος ότι... / Σίγουρα... | «Σίγουρος» = confident, «βέβαιος» = certain. |
| Είναι ενδιαφέρον το γεγονός ότι... | (αποφεύγεται) | Περιφραστικό: ξεκίνα κατευθείαν με το νόημα. |
| στατιστικά λεπτό | ανεπαρκούς μεγέθους | Βλ. §12. |

### 14. Ενεργή κριτική ανάγνωση — ο αυτοματισμός δεν αρκεί

Ο αυτοματοποιημένος έλεγχος εντοπίζει συγκεκριμένες λέξεις και σημεία στίξης. Δεν εντοπίζει:
- Αφύσικη σύνταξη (σωστές λέξεις, λανθασμένη δομή πρότασης)
- Calques (βλ. §12)
- Αγγλισμούς που δεν βρίσκονται στη λίστα
- Ρυθμό και φυσικότητα κειμένου

**Υποχρέωση:** Πριν παραδοθεί οποιοδήποτε ελληνικό κείμενο — σε αρχείο ή στην κονσόλα — διαβάζεται ολόκληρο με κριτικό μάτι ως εάν να ήταν γραμμένο από ξένο. Η ερώτηση δεν είναι «πέρασε τον έλεγχο;» αλλά «ακούγεται φυσικά ελληνικά;».

Το αυτόματο pass είναι **ελάχιστη προϋπόθεση**, όχι πιστοποίηση ποιότητας.

---

### 15. Τηλεγραφικές φράσεις — αποφεύγε τη σύνταξη «ουσιαστικό + μετοχή»

Στα αγγλικά είναι σύνηθες να γράφεται «Skill updated», «Task done», «Memory saved» ως σύντομη ανακοίνωση. Στα ελληνικά το αντίστοιχο ακούγεται ξένο· χρειάζεται πλήρης πρόταση με ρήμα.

| Λάθος (τηλεγραφικό) | Σωστό |
|---|---|
| Skill ενημερωμένο | Το Skill ενημερώθηκε. |
| Αρχείο αποθηκευμένο | Το αρχείο αποθηκεύτηκε. |
| Μνήμη ενημερωμένη | Η μνήμη ενημερώθηκε. |
| Εργασία ολοκληρωμένη | Η εργασία ολοκληρώθηκε. |
| Έγγραφο παραδοτέο | Το έγγραφο παραδόθηκε. |

**Κανόνας:** Κάθε ελληνική ανακοίνωση πρέπει να έχει ρήμα. Ουσιαστικό + μετοχή/επίθετο χωρίς ρήμα είναι αγγλικισμός.

---

## Activation Reminder

These rules apply to ALL output without exception:
- No em dashes or en dashes, ever, in any language.
- No banned phrases.
- Greek rules apply to every Greek sentence, including Claude's own explanatory
  prose in responses. Not just the "main deliverable": every sentence, every turn.
- Run the PRE-OUTPUT VERIFICATION checklist at the top of this file before
  emitting any prose response and before writing any file containing prose.
  This applies to embedded strings inside scripts (python-docx, JSON, etc.)
  exactly as it applies to the chat response. Skipping the scan because the
  Greek text is "inside code" is the most common failure mode for this skill.
- An automated check passing does not mean the text is good Greek. Read it.
