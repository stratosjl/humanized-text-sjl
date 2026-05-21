# `settings.json` hook entry

`~/.claude/settings.json` is **not** part of this repo (it carries OS-specific absolute paths and per-machine permission allowlists). When setting up a new machine, manually wire the PreToolUse hook for `greek_text_check.py`.

## Windows (already configured on the laptop)

```json
"PreToolUse": [
  {
    "matcher": "Write|Edit",
    "hooks": [
      {
        "type": "command",
        "command": "python C:/Users/StratosLaspas/.claude/scripts/greek_text_check.py",
        "timeout": 10
      }
    ]
  }
]
```

Notes:
- `python` resolves via PATH to `C:\Python314\python.exe` on this machine. The Microsoft Store `python3` alias is unusable (silent stub), do not switch to it.
- The path uses forward slashes inside the JSON string; Windows accepts both forms.

## Manjaro (TODO when first setting up)

```json
"PreToolUse": [
  {
    "matcher": "Write|Edit",
    "hooks": [
      {
        "type": "command",
        "command": "python /home/<user>/.claude/scripts/greek_text_check.py",
        "timeout": 10
      }
    ]
  }
]
```

Replace `<user>` with the actual login (Linux does not expand `~` inside this JSON string). On Manjaro the default `python` is Python 3.x via pacman, no Microsoft Store stub problem.

## Why not just put the whole settings.json in the repo

- It contains absolute, OS-specific paths (`C:\Users\...` vs `/home/<user>/...`).
- It can carry per-machine permission allowlists for `tools.allow`.
- It can carry per-machine API tokens for marketplaces (treat any such tokens as secrets, do not commit, rotate if leaked).

If you ever feel the temptation to put it in the repo, instead extract the few stable parts (hook commands written with `$HOME`-style placeholders) into a templated `settings.template.json` here, and have a small bootstrap script render it per-machine. Out of scope for now since two machines do not justify the indirection.
