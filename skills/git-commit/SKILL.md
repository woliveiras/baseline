---
name: git-commit
description: Create a safe atomic local Git commit from a verified task-owned slice using Conventional Commits. Use when local commit authority is present or the repository contract makes local commits the default; do not use for push, amend, rebase, merge, tag, release, or history rewriting.
---

# Git Commit

1. Inspect `git status --short`, unstaged diff, staged diff, and untracked files before touching the index. Identify pre-existing staged and unrelated state.
2. Select one coherent slice containing its implementation, tests, required docs, spec/matrix updates, and fresh evidence. Never use `git add .`.
3. Stage explicit task-owned paths or hunks. Do not unstage, overwrite, or absorb user-owned changes.
4. Re-read the complete cached diff. Exclude generated, secret-bearing, local, ignored, unrelated, or ambiguous content.
5. Confirm required receipts when the project opted into them. The receipt must bind the current spec, matrix, test and implementation trees, evidence, documentation decision, and three review phases. It proves integrity and declared ordering relationships, not semantic quality or actual chronology.
6. Derive `type(scope): imperative subject` from the cached diff. Keep the subject under 72 characters and add a body when decision, evidence, or migration context matters.
7. Commit locally, then show the short hash and `git show --stat --oneline --no-renames HEAD`.

Never infer authority for push, force-push, amend, rebase, merge, tag, release, publication, deploy, production, or destructive cleanup. If pre-existing staged state overlaps the slice and safe hunk isolation is unavailable, leave it untouched and report the blocker.
