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
need 'id="apDraftEmail"'
need 'const CLIENT_CONTACT'
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
# a built page (not the template) must carry the entire prompt and test plan, not one sentence
case "$FILE" in
  */template/*) ;;
  *)
    plen=$(python3 - "$FILE" <<'PYEOF'
import re,sys
s=open(sys.argv[1]).read()
m=re.search(r"^const NEXT_PROMPT\s*=\s*(.*?)^const ",s,flags=re.S|re.M)
print(len(m.group(1)) if m else 0)
PYEOF
)
    if [ "${plen:-0}" -ge 1500 ]; then echo "ok      NEXT_PROMPT holds the whole prompt and test plan ($plen characters)"; else echo "SHORT   NEXT_PROMPT is $plen characters; it must be the entire prompt and test plan (reference/next-prompt.md)"; fail=1; fi
    ;;
esac
# the script block must parse
tmp="$(mktemp -t wt_check).js"
awk '/<script>/{c=1; next} /<\/script>/{c=0} c' "$FILE" > "$tmp"
if node --check "$tmp" 2>/dev/null; then echo "ok      script parses"; else echo "BROKEN  script does not parse"; node --check "$tmp" 2>&1 | head -5; fail=1; fi
rm -f "$tmp"
# the real stage element must survive (2026-11-11: a builder cut from the comment that
# mentions <div id="stage">, the stage was lost, and the page showed only a giant logo)
stages=$(grep -c '^<div id="stage">$' "$FILE")
if [ "$stages" = 1 ]; then echo "ok      one <div id=\"stage\"> element"; else echo "BROKEN  found $stages <div id=\"stage\"> lines; the stage element is missing or doubled"; fail=1; fi
# the comment that names the stage must still be closed
if grep -q 'inside <div id="stage">: the stage is what scales' "$FILE"; then echo "ok      stage comment intact"; else echo "BROKEN  the template comment above the stage was cut; the stage was probably spliced from the wrong place"; fail=1; fi
# captured Mantine screens need the light colour scheme on <html>
if head -3 "$FILE" | grep -q 'data-mantine-color-scheme="light"' || ! grep -q 'mantine-' "$FILE"; then echo "ok      light colour scheme (or no Mantine screens)"; else echo "BROKEN  captured Mantine screens but <html> has no data-mantine-color-scheme=\"light\""; fail=1; fi
# the engine overwrites #apSubtitle with textContent, so any markup put inside it vanishes
# (2026-11-11: open questions were put there and never showed)
if grep -qE '<div class="ap-sub" id="apSubtitle">[^<]*</div>' "$FILE"; then echo "ok      review subtitle holds no markup"; else echo "BROKEN  #apSubtitle holds markup; the engine replaces it at start, so put open questions in their own element after it"; fail=1; fi
if [ "$fail" = 0 ]; then echo "PASS $FILE"; else echo "FAIL $FILE"; fi
exit $fail
