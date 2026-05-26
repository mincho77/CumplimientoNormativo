# LLM Wiki Scaffold

This vault now includes a working scaffold for the LLM Wiki pattern.

## Start Here
- Schema and rules: `AGENTS.md`
- Catalog: `wiki/operations/index.md`
- Timeline: `wiki/operations/log.md`
- Templates: `templates/`
- Helper CLI: `scripts/wiki.sh`

## Typical Flow
1. Put a new source in `raw/inbox/`.
2. Run: `scripts/wiki.sh ingest raw/inbox/<file>`
3. Ask your LLM agent to process it using `AGENTS.md`.
4. Ask questions; persist valuable answers in `wiki/analyses/`.
5. Periodically run: `scripts/wiki.sh lint`

## Notes
- `raw/` is immutable source-of-truth.
- `wiki/` is LLM-maintained synthesis.
