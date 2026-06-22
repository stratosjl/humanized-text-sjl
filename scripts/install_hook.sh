#!/usr/bin/env bash
# install_hook.sh - idempotently wire greek_text_check.py as a Claude Code
# PreToolUse(Write|Edit) hook on Linux / macOS.
#
# Why this exists: the hook only enforces if it is registered in
# ~/.claude/settings.json. Documenting the manual step proved unreliable (a
# machine can run for months with the hook unwired and no enforcement). Run
# this once per machine; it is safe to re-run.
#
# Usage:  bash scripts/install_hook.sh
set -euo pipefail

REPO_SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/greek_text_check.py"
CLAUDE_DIR="${HOME}/.claude"
SCRIPTS_DIR="${CLAUDE_DIR}/scripts"
TARGET="${SCRIPTS_DIR}/greek_text_check.py"
SETTINGS="${CLAUDE_DIR}/settings.json"

command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 not on PATH" >&2; exit 1; }
[ -f "$REPO_SCRIPT" ] || { echo "ERROR: cannot find $REPO_SCRIPT" >&2; exit 1; }

mkdir -p "$SCRIPTS_DIR"
ln -sf "$REPO_SCRIPT" "$TARGET"
echo "linked: $TARGET -> $REPO_SCRIPT"

# Merge the PreToolUse hook into settings.json without disturbing other keys.
python3 - "$SETTINGS" "$TARGET" <<'PY'
import json, os, sys
settings_path, target = sys.argv[1], sys.argv[2]
cmd = f"python3 {target}"
data = {}
if os.path.isfile(settings_path):
    with open(settings_path, encoding="utf-8") as f:
        try: data = json.load(f)
        except Exception: data = {}
    bak = settings_path + ".bak"
    with open(bak, "w", encoding="utf-8") as f: json.dump(data, f, indent=1, ensure_ascii=False)
hooks = data.setdefault("hooks", {})
pre = hooks.setdefault("PreToolUse", [])
def has_cmd(entries):
    for e in entries:
        for h in e.get("hooks", []):
            if "greek_text_check.py" in str(h.get("command", "")): return True
    return False
if has_cmd(pre):
    print("already wired: PreToolUse greek_text_check.py present, nothing to do")
else:
    pre.append({"matcher": "Write|Edit",
                "hooks": [{"type": "command", "command": cmd, "timeout": 10}]})
    os.makedirs(os.path.dirname(settings_path), exist_ok=True)
    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    print(f"wired: PreToolUse Write|Edit -> {cmd}")
PY

echo "smoke test (em dash should BLOCK):"
printf '{"tool_name":"Write","tool_input":{"file_path":"/tmp/sjl_smoke.md","content":"a — b"}}' \
  | python3 "$TARGET" >/dev/null 2>&1 && echo "  UNEXPECTED pass" || echo "  OK blocked (exit 2)"
echo "smoke test (clean should PASS):"
printf '{"tool_name":"Write","tool_input":{"file_path":"/tmp/sjl_smoke.md","content":"a, b and c"}}' \
  | python3 "$TARGET" >/dev/null 2>&1 && echo "  OK passed (exit 0)" || echo "  UNEXPECTED block"
echo "Done. Restart Claude Code so it reloads settings.json."
