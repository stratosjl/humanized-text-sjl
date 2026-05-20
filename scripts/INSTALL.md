# greek_text_check.py — install guide

This PreToolUse hook enforces the humanized-text-sjl Greek-text rules at write time. When Claude Code attempts a `Write` or `Edit` on a `.md` / `.txt` file and the new content contains em dashes, comma+`και`, English-style inner semicolons, hard-block English terms, or Greek-to-Greek violations (Rule §16), the hook returns exit code 2 and Claude must fix the issues before the write goes through.

Requirements: Python 3.10+ on PATH. No external dependencies. The script is pure stdlib.

## Linux / macOS

```bash
# 1. Copy the script into your Claude Code config dir.
mkdir -p ~/.claude/scripts
cp scripts/greek_text_check.py ~/.claude/scripts/
chmod +x ~/.claude/scripts/greek_text_check.py

# 2. Smoke test (standalone mode).
echo 'Σημείο εκκρεμές — έλεγχος' > /tmp/sjl_test.md
~/.claude/scripts/greek_text_check.py --standalone /tmp/sjl_test.md
# Expected: [BLOCK] with em_dash + greek_preferred_term findings, exit 2.

# 3. Wire up the hook in ~/.claude/settings.json
#    (merge into existing settings; do not overwrite).
```

`~/.claude/settings.json` snippet:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 $HOME/.claude/scripts/greek_text_check.py"
          }
        ]
      }
    ]
  }
}
```

## Windows (PowerShell 7+)

```powershell
# 1. Copy the script.
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\scripts" | Out-Null
Copy-Item scripts\greek_text_check.py "$env:USERPROFILE\.claude\scripts\" -Force

# 2. Smoke test (standalone mode).
$env:PYTHONIOENCODING = "utf-8"
$tmp = [System.IO.Path]::GetTempFileName() + ".md"
'Σημείο εκκρεμές — έλεγχος' | Out-File -FilePath $tmp -Encoding utf8
python "$env:USERPROFILE\.claude\scripts\greek_text_check.py" --standalone $tmp
Remove-Item $tmp
# Expected: [BLOCK] with em_dash + greek_preferred_term findings, exit 2.

# 3. Wire up the hook in %USERPROFILE%\.claude\settings.json
#    (merge into existing settings; do not overwrite).
```

`%USERPROFILE%\.claude\settings.json` snippet (note `python`, not `python3`, on Windows; `python3` resolves to the Microsoft Store stub and silently fails):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python %USERPROFILE%\\.claude\\scripts\\greek_text_check.py"
          }
        ]
      }
    ]
  }
}
```

## Optional: scope the hook to specific project trees

By default the hook fires on every `.md` / `.txt` write that is not in an exempt path segment. To restrict it to specific project sub-trees, set `HUMANIZED_TEXT_ENFORCE_ROOTS` (comma-separated path substrings) in your shell profile or Claude Code env config:

```bash
# Linux / macOS — ~/.bashrc / ~/.zshrc
export HUMANIZED_TEXT_ENFORCE_ROOTS="MyClientFolder,SharedDocs"
```

```powershell
# Windows — PowerShell profile
$env:HUMANIZED_TEXT_ENFORCE_ROOTS = "MyClientFolder,SharedDocs"
```

You can also override the default exempt segments:

```bash
export HUMANIZED_TEXT_EXEMPT_SEGMENTS="/memory/,/.claude/,/.git/,/draft/"
```

Defaults are: `/memory/`, `/.claude/`, `/.git/`, `/node_modules/`, `/Plugins/`, `/HANDOVER`.

## Verifying installation

Pick any project under an enforced root and ask Claude Code to write a Greek line containing «εκκρεμές» or `—`. The Write tool call should be blocked with a `BLOCKED by humanized-text-sjl greek_text_check` message listing the specific rule violations.

To temporarily disable the hook for a session without uninstalling it, comment out the `PreToolUse` block in `settings.json` and restart Claude Code.

## Updating

The hook ships in this repo at `scripts/greek_text_check.py`. After `git pull`, re-run the copy step from the install snippet above (Linux/macOS or Windows as appropriate). The script is self-contained, so there is no migration step.

If you installed via a junction or symlink (so the runtime script always tracks the repo), no re-copy is needed:

```bash
# Linux / macOS
ln -sf "$PWD/scripts/greek_text_check.py" ~/.claude/scripts/greek_text_check.py
```

```powershell
# Windows (Junction, no admin needed for files via mklink; use New-Item -ItemType SymbolicLink for true symlink with admin)
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\scripts\greek_text_check.py" -Target "$PWD\scripts\greek_text_check.py" -Force
```
