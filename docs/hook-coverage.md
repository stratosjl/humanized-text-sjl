# Hook coverage: the check sees tool calls, not files

`scripts/greek_text_check.py` is designed to be wired as a **PreToolUse** hook on the
file-writing tools. That is the right place for it to run, and it has one consequence
worth stating plainly, because a silent gap in a backstop is worse than no backstop.

## The limitation

A PreToolUse hook fires on a **tool call**. It does not see a file. So a file created by
any route that is not one of the hooked tools is never inspected:

- a shell heredoc (`cat > file <<'EOF'`, `python3 - <<'PY'`) run through a command tool
- a script that writes files as a side effect
- `Set-Content` or `[System.IO.File]::WriteAllText` on Windows
- anything a build step or a generator produces

Measured in practice: in a working session where the hook fired twice and blocked two
writes, the great majority of that session's prose edits were made through shell heredocs
and were never inspected at all. **The two blocks made the guard feel present while most of
the output bypassed it.** That is the failure mode to guard against, because previous green
results train the writer to trust the path.

## What follows

**Decide by destination, not by tool.** Any file that will contain prose should get the
check before it is written, regardless of which mechanism writes it. Treat the hook as one
of several places the check can run, not as the guarantee.

Options, in rough order of cost:

1. **Also fire on the command tool**, inspecting heredocs and redirections whose target
   looks like prose. Cheap to describe, awkward to parse reliably, and it will have false
   negatives.
2. **Move to a PostToolUse or session-end hook** that inspects files *changed* during the
   turn, by path rather than by tool. This decides by destination, which is the property
   that actually matters.
3. **Add a pre-commit hook** in repositories that receive prose. Catches every route,
   including ones nobody anticipated, at the cost of catching them later.

None of these is free, and (1) is the one most likely to give a false sense of coverage,
because it looks complete and is not.

## The general shape

This is worth recognising beyond this script: **a control bound to a tool guards that tool,
not the outcome.** Whenever a check is attached to how something is done rather than to what
is produced, ask which other routes reach the same outcome, and whether the check's green
results will be read as covering them.
