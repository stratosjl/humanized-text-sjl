# Greek scan patterns and hard-block terms

Part of the `humanized-text` skill. Load this during Pass 1 whenever the output
contains Greek. Rule numbers reference `references/greek-rules.md`.

### Greek scan patterns (highest-frequency errors)

| Trigger pattern in the draft | Likely error | Fix |
|---|---|---|
| Deponent verb form `…ίζονται από` / `…εύονται από` / `…ούνται από` | Deponent abused as true passive (Rule §2 below) | Use nominalisation (`τη διαχείριση έχει αναλάβει η Χ`, `γίνεται διαπραγμάτευση`) or true passive (`υποβάλλεται`, `εξετάζεται`) |
| `διαχειρίζονται από` | The single most common error in financial/maritime Greek | `υπό τη διαχείριση της Χ` / `τη διαχείρισή τους έχει αναλάβει η Χ` |
| `επεξεργάζονται από` | Same | `υπόκεινται σε επεξεργασία από` / `τα επεξεργάζεται η Χ` |
| `διαπραγματεύονται από` | Same | `αποτελούν αντικείμενο διαπραγμάτευσης από` |
| `ασχολούνται από` | Same | `εξετάζονται από` / `αντιμετωπίζονται από` |
| Acronym followed by Greek noun without article (`HTML αναφορά`, `GDPR απαιτήσεις`) | Anglicism word order (Rule §3) | `αναφορά κατά την HTML` / `απαιτήσεις του GDPR` |
| Acronym used as grammatical subject without article (`GDPR προβλέπει`, `AI Act απαιτεί`) | Missing definite article (Rule §5) | `ο GDPR προβλέπει`, `ο AI Act απαιτεί` |
| Foreign noun before Greek noun (`το Orders πίνακας`, `API documentation εργασία`) | Foreign modifier in head position (Rule §6) | Greek noun first: `ο πίνακας Orders`, `εργασία πάνω στο API documentation` |
| Foreign compound modifier before Greek head (`real-time επεξεργασία`) | Same family (Rule §6 Pattern B) | Greek noun first: `επεξεργασία real-time` |
| Brand/foreign-name without article (`από Apple`, `μέσω Google`, `μέσω BBC`) | Missing definite article (Rule §5) | `από την Apple`, `μέσω της Google`, `μέσω του BBC` |
| `—` anywhere | Em dash banned in any language (formatting rule) | Replace with `:`, `,`, `(...)`, plain hyphen, or restructure |
| Mixed-language compound abbreviations as bullet headers (`Sanctions / PEP screening:`) | Foreign-only header in Greek prose | Greek-first restructure: `Έλεγχος κυρώσεων και PEP (sanctions / PEP screening):` |
| `!».` or `;».` (terminal punctuation inside the quotes AND a full stop after) | Double terminal punctuation (Rule §20.3) | Drop the outer full stop: `«...!».` becomes `«...!»` |
| `, και` anywhere in Greek text | Anglicism (Oxford comma; banned by Rule §7) | Remove the comma: `, και` → ` και` |
| `, ή` anywhere in Greek text | Same anglicism, the most common escape (Rule §7) | Remove the comma: `, ή` → ` ή` |
| `, ούτε` / `, είτε` / `, καθώς και` | Same anglicism on the other coordinating conjunctions (Rule §7) | Remove the comma |
| `;` mid-sentence followed by lowercase Greek letter | English semicolon misused as άνω τελεία (Rule §8) | Replace `;` with `·` (U+0387), keep no leading space |
| `αμφίπλευρ*` referring to two-party relations / agreements / documents | Wrong word for "bilateral" (Rule §9) | Replace with `διμερ*` (διμερής, διμερή, διμερείς) |
| English legal or business term used as Greek prose noun | Anglicism in Greek prose (Rule §11) | Use Greek equivalent from the table in Rule §11 |
| Greek noun/article + Greek participle/adjective with no conjugated verb (`Skill ενημερωμένο`) | Telegraphic anglicism (Rule §15) | Full Greek sentence with conjugated verb: `Το Skill ενημερώθηκε` |
| `εκκρεμές` (αυτόνομη χρήση ως κατηγορούμενο) | Λόγια διατύπωση (Rule §16) | `σε εκκρεμότητα` (`παραμένει σε εκκρεμότητα`) |
| `διάδρομος επικοινωνίας` | Calque (Rule §16) | `κανάλι επικοινωνίας` |
| `να είμαι καθαρός` / `να είμαστε καθαροί` (δήλωση σαφήνειας) | Calque του «let me be clear» (Rule §16) | `για να είμαι σαφής` / `για να είμαστε σαφείς` |
| `είναι καθαρό ότι/πως` | Calque του «it's clear that» (Rule §16) | `είναι σαφές ότι` / `είναι ξεκάθαρο ότι` |
| «Ροή 2», «Κανόνας 3», «Φάση 1» (ουσιαστικό-ετικέτα σειράς με απόλυτο αριθμητικό μετά) | Απόλυτο αντί τακτικού σε αριθμημένη σειρά (Rule §18) | Τακτικό: «Ροή 2η» ή «δεύτερη ροή». Εξαίρεση: παραπομπές (άρθρο 27, παρ. 1, ΦΕΚ 235) |
| «Η παρ. 6 ... και η παρ. 4 ... περιλαμβάνουν», «Το άρθρο 90 και το άρθρο 116 ... αντικαθιστούν» (ενικό άρθρο, το ίδιο ουσιαστικό ξανά μετά το «και», ρήμα στον πληθυντικό) | Το υποκείμενο διαβάζεται ενικό ενώ το ρήμα είναι στον πληθυντικό (Rule §21) | Το κοινό ουσιαστικό μία φορά στον πληθυντικό: «Οι παρ. 6 ... και 4 ... περιλαμβάνουν», «Τα άρθρα 90 και 116 ... αντικαθιστούν» |

### Hard-block terms reference

The following English terms commonly appear in Greek professional prose but should be
replaced with their Greek equivalents. Extend this list with your own overrides.

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

Technical terms anchored in specific regulatory frameworks (e.g. audit trail, due
diligence, outsourcing, threshold, tipping-off) may remain in their original form
when used as defined terms in their framework context.

### Scope reminder

These checks apply equally to:
- Direct prose responses to the user.
- Strings inside generated code (e.g. Greek text inside `add_para("...")` calls in
  python-docx scripts that build .docx files for the user).
- Headings, table cell text, footers, captions, and metadata fields.
- Email drafts, letters, memos, policy documents, and any deliverable the user may
  forward to a third party.

If you only check the chat-level prose and skip the embedded strings, the
deliverable will fail. Always scan the artefact's text content, not just the
covering message.
