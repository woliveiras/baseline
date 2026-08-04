# Enforcement boundary

Tuxedo uses the current Codex plugin hook location, `hooks/hooks.json`, without a manifest override. Plugin hooks are non-managed: Codex skips them until the user reviews and trusts the current definition.

## Enforced mechanically

- Reject malformed hook input rather than guessing on a protected event.
- Block a narrow catalog of broad, difficult-to-recover commands.
- Require an exact SHA-256 command grant for push, release, deploy, production, and destructive commands that are not categorically blocked.
- When `.tuxedo/policy.json` opts in, require named receipt artifacts and verify their SHA-256 hashes before `git commit` or turn completion.
- Keep hook execution local and deterministic; use no network and emit no file contents.

## Not enforced

- The semantic quality or completeness of a spec, test, review, or architecture.
- Whether a grant was actually authored by a human; the hook can validate only the presence and exact command hash of a local grant.
- Commands hidden behind aliases, custom binaries, hosted tools, unsupported tool paths, or future schema changes.
- Effects that already occurred before a `PostToolUse` hook.
- Completion outside a trusted and enabled Codex hook runtime.

`Stop` can request another continuation; it cannot prove that the final result is correct. Projects that need stronger organizational enforcement must use managed policy outside this plugin.

## Receipt contract

Copy `templates/policy/policy.json` to `.tuxedo/policy.json` to opt in. A receipt names the spec, behavior matrix, evidence record, and every artifact whose current bytes must match a recorded SHA-256 hash. Metadata routes the check; reviewers still read the full artifacts.
