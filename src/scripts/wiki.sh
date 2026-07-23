#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INDEX="$ROOT_DIR/wiki/operations/index.md"
LOG="$ROOT_DIR/wiki/operations/log.md"
TODAY="$(date +%F)"

usage() {
  cat <<USAGE
Usage:
  scripts/wiki.sh ingest <raw/inbox/filename>
  scripts/wiki.sh query <question text>
  scripts/wiki.sh lint
USAGE
}

log_event() {
  local mode="$1"
  local title="$2"
  shift 2
  {
    echo "## [$TODAY] $mode | $title"
    for line in "$@"; do
      echo "- $line"
    done
    echo
  } >> "$LOG"
}

ensure_files() {
  [[ -f "$INDEX" ]] || { echo "Missing $INDEX"; exit 1; }
  [[ -f "$LOG" ]] || { echo "Missing $LOG"; exit 1; }
}

cmd_ingest() {
  local src="${1:-}"
  if [[ -z "$src" ]]; then
    echo "ingest requires a source path"
    usage
    exit 1
  fi
  if [[ ! -f "$ROOT_DIR/$src" ]]; then
    echo "Source file not found: $src"
    exit 1
  fi

  log_event "ingest" "$src" \
    "Source queued for LLM processing." \
    "Next step: create/update source/entity/concept pages and index entries."

  echo "Ingest logged for: $src"
  echo "Now ask your LLM agent: ingest '$src' following AGENTS.md workflow."
}

cmd_query() {
  local question="${*:-}"
  if [[ -z "$question" ]]; then
    echo "query requires text"
    usage
    exit 1
  fi

  log_event "query" "$question" \
    "Question recorded." \
    "If answer has lasting value, persist into wiki/analyses/."

  echo "Query logged. Ask LLM to answer from wiki and optionally persist analysis page."
}

cmd_lint() {
  local orphan_count
  orphan_count="$(rg -n "\[\[[^]]+\]\]" "$ROOT_DIR/wiki" --glob '*.md' | wc -l | tr -d ' ')"

  log_event "lint" "wiki health check" \
    "Basic link-scan lines found: $orphan_count" \
    "Run deeper LLM lint for contradictions, stale claims, and missing pages."

  echo "Lint logged. Use LLM for semantic lint pass per AGENTS.md."
}

main() {
  ensure_files
  local cmd="${1:-}"
  shift || true
  case "$cmd" in
    ingest) cmd_ingest "$@" ;;
    query) cmd_query "$@" ;;
    lint) cmd_lint ;;
    *) usage; exit 1 ;;
  esac
}

main "$@"
