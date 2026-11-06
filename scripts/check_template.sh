#!/usr/bin/env bash
# Checks the walkthrough template (or any page built from it) for the version-2 review card:
# three choices (Approved / Approve with the following changes / Denied), an assignee list,
# the relay settings, a send timeout, and a script block that parses.
# Usage: scripts/check_template.sh [path-to-html]   (default: template/walkthrough-template.html)
set -u
HERE="$(cd "$(dirname "$0")/.." && pwd)"
FILE="${1:-$HERE/template/walkthrough-template.html}"
fail=0
need() {
  if grep -qF -- "$1" "$FILE"; then echo "ok      $1"; else echo "MISSING $1"; fail=1; fi
}
absent() {
  if grep -qF -- "$1" "$FILE"; then echo "PRESENT $1 (must be gone)"; fail=1; else echo "ok      no $1"; fi
}
need 'Approve with the following changes'
need '>Denied<'
need 'id="apAssign"'
need 'const ASSIGNEES'
need 'const REVIEWER'
need 'const FEEDBACK_ENDPOINT'
need 'const FEEDBACK_KEY'
need 'const PAGE_PATH'
need 'const WALKTHROUGH_URL'
need 'const NEXT_PROMPT'
need 'const TEMPLATE_VERSION = 2'
need 'submission_id'
need 'Not posted to Slack'
need "reject:'DENIED'"
absent 'data-v="changes"'
absent 'const WEBHOOK_URL'
# the script block must parse
tmp="$(mktemp -t wt_check).js"
awk '/<script>/{c=1; next} /<\/script>/{c=0} c' "$FILE" > "$tmp"
if node --check "$tmp" 2>/dev/null; then echo "ok      script parses"; else echo "BROKEN  script does not parse"; node --check "$tmp" 2>&1 | head -5; fail=1; fi
rm -f "$tmp"
if [ "$fail" = 0 ]; then echo "PASS $FILE"; else echo "FAIL $FILE"; fi
exit $fail
