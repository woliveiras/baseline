---
name: git-commit
description: Create a safe atomic local Git commit from a verified task-owned slice using Conventional Commits. Use only when the user explicitly requests a local commit or explicitly asks to follow a repository contract that requires one; do not use when the request says not to commit, or for push, amend, rebase, merge, tag, release, or history rewriting.
---

# Git Commit

1. Inspect `git status --short`, unstaged diff, staged diff, and untracked files before touching the index. Identify pre-existing staged and unrelated state.
2. Select one coherent slice containing its implementation, tests, required durable documentation, and fresh validation results. Never use `git add .`.
3. Stage explicit task-owned paths or hunks. Do not unstage, overwrite, or absorb user-owned changes.
4. Re-read the complete cached diff. Exclude generated, secret-bearing, local, ignored, unrelated, or ambiguous content.
5. Compare the cached candidate with the authorized task, governing input, tests, validation results, documentation decision, and completed review. Stop if ownership or scope is ambiguous.
6. Derive `type(scope): imperative subject` from the cached diff. Keep the subject under 72 characters and add a body when decision, evidence, or migration context matters.
7. Commit locally, then show the short hash and `git show --stat --oneline --no-renames HEAD`.

Never infer authority for push, force-push, amend, rebase, merge, tag, release, publication, deploy, production, or destructive cleanup. If pre-existing staged state overlaps the slice and safe hunk isolation is unavailable, leave it untouched and report the blocker.
