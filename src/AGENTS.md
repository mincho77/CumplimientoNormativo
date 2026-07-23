# AGENTS.md — LLM Wiki Operating Schema

This vault uses an LLM-maintained, persistent wiki workflow.

## Mission
- Maintain a compounding knowledge base for **cumplimiento normativo**.
- Treat `raw/` as immutable source-of-truth.
- Write and maintain all synthesized knowledge in `wiki/`.

## Non-Negotiables
1. Never edit files inside `raw/`.
2. Every meaningful operation must append an entry to `wiki/operations/log.md`.
3. Every new or updated wiki page must be reflected in `wiki/operations/index.md`.
4. Prefer updating existing pages over creating duplicates.
5. Flag contradictions explicitly; do not silently overwrite claims.
6. Use explicit dates in ISO format (`YYYY-MM-DD`).

## Directory Contract
- `raw/inbox/`: newly added sources pending ingestion.
- `raw/processed/`: optional archive location for ingested sources.
- `raw/assets/`: local images/files associated with sources.
- `wiki/sources/`: one page per ingested source.
- `wiki/entities/`: institutions, laws, regulators, standards, actors.
- `wiki/concepts/`: themes, frameworks, obligations, risk concepts.
- `wiki/analyses/`: query outputs worth preserving.
- `wiki/operations/index.md`: catalog of wiki pages.
- `wiki/operations/log.md`: append-only operation log.

## Naming Conventions
- Source page: `wiki/sources/YYYY-MM-DD - <short-title>.md`
- Entity page: `wiki/entities/<entity-name>.md`
- Concept page: `wiki/concepts/<concept-name>.md`
- Analysis page: `wiki/analyses/YYYY-MM-DD - <analysis-title>.md`
- Use lowercase kebab-case only if a filesystem requires it; otherwise preserve readable titles.

## Page Frontmatter Standard
Use this frontmatter on all wiki pages:

```yaml
---
title: "..."
type: source | entity | concept | analysis
status: draft | stable | superseded
created: YYYY-MM-DD
updated: YYYY-MM-DD
source_files: []
source_count: 0
confidence: low | medium | high
tags: []
---
```

## Minimum Structure by Page Type
### Source page (`type: source`)
- `## Summary`
- `## Key Claims`
- `## Evidence / Data`
- `## Extracted Entities`
- `## Extracted Concepts`
- `## Open Questions`
- `## Links`

### Entity page (`type: entity`)
- `## Overview`
- `## Relevant Obligations / Roles`
- `## Related Concepts`
- `## Source Trail`
- `## Contradictions / Uncertainties`

### Concept page (`type: concept`)
- `## Definition`
- `## Why It Matters`
- `## Related Entities`
- `## Source Trail`
- `## Contradictions / Uncertainties`

### Analysis page (`type: analysis`)
- `## Question`
- `## Answer`
- `## Evidence Used`
- `## Caveats`
- `## Follow-up Actions`

## Link Policy
- Use Obsidian wikilinks (`[[Page Name]]`) for internal references.
- Prefer at least 3 outbound links for non-trivial pages.
- When introducing a new entity/concept without a page, create a stub page during the same operation.

## Ingest Workflow (single source)
1. Identify one file from `raw/inbox/`.
2. Read and summarize.
3. Create/update corresponding source page in `wiki/sources/`.
4. Update affected entity/concept pages.
5. Add missing stubs for newly discovered key entities/concepts.
6. Update `wiki/operations/index.md`.
7. Append ingest event to `wiki/operations/log.md`.

## Query Workflow
1. Read `wiki/operations/index.md` first.
2. Identify relevant pages and synthesize answer from wiki first.
3. If answer adds lasting value, create an analysis page in `wiki/analyses/`.
4. Update index and append query event to log.

## Lint Workflow
Run periodic checks for:
- Orphan pages (no inbound links).
- Duplicate pages covering same concept/entity.
- Stale claims superseded by newer sources.
- Missing concept/entity pages referenced repeatedly.
- Broken links.

Record lint findings in log with prioritized remediation actions.

## Contradiction Handling
When new evidence conflicts with prior synthesis:
- Preserve both claims with source attribution.
- Mark older claim as potentially superseded.
- Add explicit note under `## Contradictions / Uncertainties`.
- If resolved, note rationale and date.

## Citation Style
- Cite source pages inline as wikilinks, e.g. `[[2026-05-25 - Circular SFC X]]`.
- For direct factual claims, include a short quote or pinpoint section if available.

## Operational Modes
- `ingest <filename>`: process one source.
- `query <question>`: answer from wiki and optionally persist as analysis.
- `lint`: health-check wiki and propose fixes.

## Quality Bar
- Prefer precision over verbosity.
- Distinguish fact vs inference explicitly.
- Keep claims auditable via source trail.
