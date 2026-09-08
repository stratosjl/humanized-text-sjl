# Shared project context

Project: `humanized-text-sjl`. Preserve existing data classification, repository routing
and machine configuration. Maintain task state in the existing records below.

[SKILL.md](SKILL.md) is the shared writing policy source. Tool adapters reference
this repository directly. Keep writing references and deterministic checks here.

## Repository synchronization

At every session start, and before work in another repository, inspect the branch,
local changes and configured remotes. Read the routing rules needed to identify
the owning remote before contacting it. Fetch that remote, compare the working
branch with its upstream, and apply a safe fast-forward when behind.

Reconcile divergence or overlapping changes before substantive review or editing.
Preserve unrelated work; do not reset, discard changes or force a push to make a
branch current. After synchronization, record the revision and reread this file
and the current task records. A fetch alone does not update working files.

If the remote is unavailable, report freshness as unverified and leave dependent
work pending. A local root outside Git keeps its recorded ownership; do not
initialize a repository to satisfy this procedure. Before publication, refresh
the remote again and reconcile intervening commits through the approved route.

Fetching cannot reveal another machine's uncommitted or unpushed work. Establish
the revision and scope of reported overlapping work before editing those files.
Keep machine-specific verification separate.

Existing project records:

- [README.md](README.md)
- [SKILL.md](SKILL.md)
