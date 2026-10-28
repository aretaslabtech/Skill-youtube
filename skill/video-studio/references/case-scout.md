# Case scout — reconstruct a real case from primary sources first

A crime-case or case-files video starts from a real investigation reconstructed from
official and primary sources, never from "what the internet says happened." The scout is a
fresh sub-agent that runs before a single line of script is written. Its job is to find a
case worth telling, build its timeline from the strongest sources available, and mark
exactly how solid every claim is — so the writer physically cannot promote a repeated
internet guess into a fact.

**Why:** generated true-crime content fails in one specific way: the model fills gaps
left by thin sources with the most common version it has seen online, and that version
is often an unsourced guess repeated by a hundred blogs. Crimen Metódico's whole premise —
reconstructing the method and the investigation, cold and documentary — depends on never
doing that.

## Case suitability (score 0–3 each, max 15; discard anything that scores 0 on *Primary
sources* or *Clear method*)

| Criterion | 0 | 3 |
|---|---|---|
| **Primary sources exist** | only secondary write-ups, nothing official | court records, police files, or declassified material are findable |
| **Clear method/pattern** | a single ambiguous incident | a documented pattern across the investigation (how they acted, how they were caught) |
| **Chronology is reconstructable** | dates conflict with no way to resolve them | contemporary press + official dates agree, or disagreements are resolvable |
| **Not sub judice / not re-victimizing** | an active trial, identifiable living minors, or a case where the only coverage sensationalizes victims | closed case, or coverage that exists can be told without naming/exposing vulnerable living people |
| **Not over-exploited** | one of the five most-covered cases on YouTube true-crime already | `ledger.py check` finds no close match in the last 90+ days, and the angle (the method, the investigative failure, the pattern) isn't the one every other channel tells |

## Source hierarchy

Build the case from the top down. Drop to a lower tier only when the tier above has
nothing on the specific claim you need.

1. **Primary / official.** Police case files and declassified material, judicial
   sentences and court filings, prosecutors'/ministries' own releases, official forensic
   or investigative reports, FOIA and public archives. Example: the FBI's own historical
   case material, including FBI Vault files (e.g. the Dahmer file).
2. **Judicial databases.** US: [CourtListener](https://www.courtlistener.com) (large free
   index of case law and court opinions). Spain: CENDOJ, BOE where relevant, the court's or
   fiscalía's own publications.
3. **Contemporary press (hemerotecas).** Local papers from the place and time of the case,
   national press, wire agencies, public newspaper archives. For older US cases,
   [Chronicling America](https://www.loc.gov/collections/chronicling-america/) (Library of
   Congress) digitizes millions of historical newspaper pages through 1963.
4. **Investigative journalism and well-documented books.** Fill gaps, interviews, context
   and reconstruction — but never outrank a judicial document when the two disagree.
5. **Documentaries and interviews.** Useful for quoted statements from investigators,
   family, journalists or witnesses. Always attributed ("X said…"), never promoted to fact.
6. **Discovery only — never a final source for a claim.** Wikipedia, Reddit, Murderpedia,
   blogs, other YouTube channels, podcasts. Good for "there's something here worth
   investigating," never for "this is what happened."

For images: a separate pass against police/public archives, Wikimedia Commons, the Library
of Congress's digitized collections (check its stated rights status for the specific
collection), and press archives with a compatible licence — plus maps and original
documents. Never an AI-generated "security cam" image presented as real footage.

## The process

1. Find a candidate case (from the rotation, the planner, or discovery-tier sources —
   discovery only decides *what to look into*, never *what happened*).
2. Locate primary/official sources for it.
3. Locate judicial records and resolutions.
4. Search contemporary press from the time and place of the case.
5. Search reliable retrospective journalism to fill remaining gaps.
6. Build a provisional chronology from what's found so far.
7. Cross-check every claim across the sources that mention it.
8. Flag contradictions explicitly — don't silently pick one.
9. Classify every factual claim (see below).
10. Only then write the script — from the ledger, not from memory of "how this case is
    usually told."

## Claim classification

Every claim that will appear in the script gets exactly one status in the evidence
ledger:

| Status | Means | Example |
|---|---|---|
| `confirmed` | A primary/official document says so, or ≥ 2 independent contemporary sources agree and nothing contradicts it | "Fue detenido el 22 de julio" → backed by a police/judicial document or contemporary press |
| `reported` | Contemporary press or a judicial record says so, but it isn't a primary document in hand | a date or detail only in period newspaper coverage |
| `alleged` | A single source, a party's claim, or a psychological/motive interpretation attributed to someone | "tenía una obsesión con X" → only valid if attributed to *who* said it |
| `disputed` | Sources genuinely disagree and the disagreement can't be resolved | two papers give different dates and no official record settles it |
| `unknown` | Can't be sourced at all | leave it out, or say on screen that it's unknown |

**The hard rule:** no claim that matters to the narrative enters the script because it
appears on a single secondary site. A detention date needs a police/judicial document or
contemporary press. A claimed motive or modus operandi needs multiple victims/the
investigation itself or a documented source — and if it's psychological interpretation
("sentía placer controlando a sus víctimas"), it goes in as an attributed opinion
("según el libro de X…") or it doesn't go in at all.

## Output

**`research/evidence-ledger.yaml`** — one entry per claim that will appear in the script:

```yaml
- claim: "La policía vinculó inicialmente cinco asesinatos al mismo autor."
  status: confirmed
  sources:
    - type: police
      url: "https://..."
    - type: contemporary_press
      url: "https://..."
  script_safe: true

- claim: "El asesino elegía a sus víctimas porque le recordaban a su madre."
  status: alleged
  sources:
    - type: book
      author: "..."
      title: "..."
  script_safe: false
  reason: "Interpretación no respaldada por fuentes primarias — solo entra como opinión atribuida."
```

**`research/case.md`** — the provisional chronology and a one-paragraph summary of why
this case and this angle, plus any contradictions flagged in step 8.

## Gate C1 (rubric, new — doesn't reuse the A/B numbering)

PLAN §1 names the case and cites the evidence ledger. Write `C1: PASS (case scout)` into
PLAN §10 only when every claim used in the script has `script_safe: true` in
`research/evidence-ledger.yaml` (an `alleged`/`disputed` claim can still be `script_safe:
true` if the script attributes it correctly — the ledger just has to say so explicitly).
`deliver.py` refuses a `crime-case` or `case-files` video without that line or without
`research/evidence-ledger.yaml`.

## Scout prompt (give it to a fresh sub-agent, nothing else)

> You are a research assistant for a true-crime documentary channel (Crimen Metódico,
> Spanish-language, adult audience) whose standard is: reconstruct real investigations from
> primary and official sources, cold and narrative, never sensationalist. Find one case
> candidate for <today's slot>, then build its chronology strictly in this order: 1)
> official/primary sources (police files, court records, FOIA, declassified material), 2)
> judicial databases (CourtListener for the US; CENDOJ/BOE for Spain), 3) contemporary press
> from the case's own time and place (use Chronicling America for pre-1964 US cases), 4)
> reliable retrospective journalism and documented books to fill gaps, 5) documentaries/
> interviews for attributed quotes only. Wikipedia, Reddit, Murderpedia, other true-crime
> channels and podcasts may only tell you *what to investigate*, never serve as your source
> for a claim. For every claim you plan to use, classify it confirmed / reported / alleged /
> disputed / unknown per the rubric below, and mark `script_safe: false` with a reason on
> anything that's a single-secondary-source claim or an unattributed psychological
> interpretation. Flag any contradiction between sources explicitly — don't silently pick
> one. Return `research/evidence-ledger.yaml` and `research/case.md` in the formats below.
> Already made (skip these cases/angles): <ledger topics, last 90+ days>.
> <classification rubric and YAML format pasted from this file>
