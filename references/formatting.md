# Formatting, pagination, and widow control

Part of the `humanized-text` skill. Load this when producing a formatted
artefact: markdown with headings, .docx, .pdf, HTML, or LaTeX.

## Formatting Rules

**No em dashes or en dashes, ever.** This is a hard rule with one narrow exemption,
the harness-dictated memory-index line (`- [title](file.md) SEPARATOR hook text`);
see the hard-rules section of SKILL.md.
Use one of these instead, depending on context:
- a colon (:) to introduce or expand
- a plain hyphen (-) for compound adjectives
- commas to enclose a parenthetical clause
- parentheses () for asides

**No space before punctuation.** Never put a space before `.` `,` `:` `;` `!` `?` `·` `»` `…`. The space follows the punctuation mark, never precedes it (`λέξη.` not `λέξη .`; `παράδειγμα:` not `παράδειγμα :`). Same for the opening Greek guillemet: write `«λέξη»`, not `« λέξη »`.

Do not use unnecessary quotation marks around ordinary words.

Do not over-format with heavy headings and bullet lists unless the user asks for a
structured outline.

Do not repeat the same opening sentence structure across responses.

**Title Case in headings is banned.** Use sentence case ("Building the redirect map"),
not Title Case ("Building The Redirect Map"). Proper nouns and acknowledged
conventions in the relevant style guide are the only exceptions.

**Do not over-bold.** Reserve bold for words the reader's eye must catch on a
re-scan: a defined term, a critical warning, a one-word answer in a Q&A.
Bolding every list item's leading phrase is a tell.

**Inline-header vertical lists are banned by default.** A bulleted list where
every item is `**Boldface header:** description sentence` is the most common
AI structural tic. Use either prose paragraphs OR a clean bullet list of short
items; do not blend the two. The two acceptable exceptions are: a comparison
matrix that genuinely needs a `key: value` shape, and a glossary.

**Use straight quotation marks.** `"Like this"`, not curly `"like this"`. Same
for apostrophes: `it's`, not `it's`. The skill assumes UTF-8 throughout; the
straight-vs-curly distinction is purely a generated-text artefact.

**Do not insert horizontal rules before headings.** Lines like `---` directly
above a `##` line are a Wikipedia-flagged AI tell. The heading is its own
visual break; trust it.

**Do not skip heading levels.** Never jump from `##` to `####`. Each level
steps down by exactly one.

---

## Pagination and widow control

These rules apply to every document that is rendered with visible pagination:
PDF (ReportLab, weasyprint, wkhtmltopdf, LaTeX), DOCX viewed in print layout,
and HTML print stylesheets. They are about how page breaks land on headings
and tables. They are not about font, colour, or spacing.

There are four rules, and all four are mandatory:

1. **Never leave a heading alone at the end of a page** with its content
   starting on the next page. Push the heading to the next page so it stays
   with at least the first paragraph (or first row) it introduces. An orphan
   heading at the bottom of a page is a reading defect: the reader has to
   page-flip to discover what it labels.
2. **Never leave the header row of a table alone at the end of a page** with
   the body rows starting on the next page. Same reasoning: a header without
   any body next to it is content-free at the place the reader's eye lands.
   Push the header to the next page so it stays with at least one body row.
3. **When a table breaks between pages, repeat the header row on each
   continuation page.** A body fragment on a fresh page without column
   labels is unreadable for any reviewer scanning the document. This is the
   single most common pagination defect in generator-produced PDFs.
4. **Never split a single row across two pages.** Keep all cells of one row
   together. If a row does not fit, push the whole row to the next page
   intact. A row whose first three cells sit on page 3 and last three cells
   sit on page 4 cannot be read at all.

These rules govern only headings and tables. They do not say anything about
mid-paragraph breaks (which are fine) or about when a section *should*
straddle pages (which is normal and desired). They exist because the failure
modes they prevent are not stylistic preferences; they are functional
breakages of the document.

### How to apply, per output format

**ReportLab (Python).** This is the most common stack for programmatic PDFs
in regulated-firm projects.

- Tables: pass `repeatRows=1` to `Table(...)` so the header row reappears on
  every continuation page.
- Tables: leave `splitByRow=True` (the default). Never set `splitInRow=True`
  or override `splitByRow` to anything that allows cell-level splits.
- Sections: set `keepWithNext=1` on the `ParagraphStyle` used for headings,
  so a heading is never the last flowable on a page.
- Heading-plus-first-table sequences: wrap them in
  `KeepTogether([heading, table, ...])` so the engine pulls both to the
  next page if the table cannot start on the current one. `KeepTogether`
  prevents the heading-orphan-then-table case that `keepWithNext` alone
  does not always catch when the heading is short and the table is long.

**python-docx (Word output).**

- Heading paragraphs: `paragraph.paragraph_format.keep_with_next = True`.
- Body paragraphs that must not break internally:
  `paragraph.paragraph_format.keep_together = True`.
- Repeating table headers: there is no high-level helper. Set
  `<w:trPr><w:tblHeader/>` on the first row of the table via lxml
  (`row._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))`). Word
  honours this on every continuation page automatically.
- Intra-row breaks: set `<w:trPr><w:cantSplit/>` on every row so Word never
  splits a row mid-page.

**HTML / CSS print stylesheets.** Use the modern `break-*` properties with
the legacy `page-break-*` fallback:

```css
h1, h2, h3, h4, h5, h6 {
  page-break-after: avoid;
  break-after: avoid-page;
}
table thead { display: table-header-group; }   /* repeats header on print */
tr {
  page-break-inside: avoid;
  break-inside: avoid;
}
```

The `display: table-header-group` rule on `thead` is what makes browsers
repeat the header on every printed page; without it most print engines drop
the header on continuation pages.

**LaTeX.** Use `\nopagebreak` after headings, `longtable` (not `tabular`)
with a `\endhead` clause for the repeating header row, and `\\*` instead of
`\\` at row ends to disallow intra-row breaks. The `booktabs` package's
documentation has the canonical pattern.

### Hard failure modes that this prevents

- A "Per-instrument disposals" heading on page 1 with the table starting on
  page 2.
- A table header `Instrument | Qty | Proceeds | Basis | Gain` on page 2,
  body starting on page 3.
- A table that breaks across pages 4 and 5 with no header on page 5, so the
  reader sees a wall of unlabelled numbers.
- A row whose long product name wraps onto a second line, with line 1 on
  page 5 and line 2 on page 6.

Each is a defect even if the totals are right.

---

## When the User Asks for Formal Tone

Use slightly more elevated vocabulary where appropriate. The banned phrases above
still apply. The difference is precision and structure, not corporate or AI-sounding
language.

