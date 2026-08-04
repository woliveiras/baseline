# Hook guardrails and enforcement boundaries

Tuxedo's hooks provide two mechanical safety checks while Codex works in a project:

1. Stop dangerous or unauthorized shell commands before they run.
2. Optionally stop a commit or turn completion when its recorded engineering evidence is missing or stale.

The hooks check commands, files, and SHA-256 hashes. They do not decide whether a specification is correct, whether tests are sufficient, or whether an architecture is good.

## When the hooks run

Tuxedo uses the standard plugin hook file at `hooks/hooks.json`. After installing or enabling the plugin, open `/hooks` in Codex, inspect the definitions, and trust them. Codex skips plugin hooks until this review is complete. If a hook definition changes, Codex requires another review because its trusted hash changed.

Two events are configured:

| Event | When it runs | What Tuxedo does |
| --- | --- | --- |
| `PreToolUse` for `Bash` | Before every shell command Codex attempts | Allows ordinary commands, blocks categorically dangerous commands, checks grants for protected commands, and checks receipts before `git commit` when enabled. |
| `Stop` | When Codex is about to finish a turn | Checks completion receipts when the project opted into the `stop` requirement. If evidence is missing or stale, asks Codex to continue instead of finishing. |

The hook may run for an ordinary command such as `python3 -m unittest`, find no protected condition, and return without interfering.

## Command protection

Commands fall into three groups.

### Ordinary commands

Commands that do not match a protected rule continue normally. Examples include focused tests, read-only Git inspection, formatting, and local builds.

```text
Codex attempts: python3 -m unittest
Hook result: no protected condition
Outcome: command runs
```

### Categorically blocked commands

The current hook always blocks broad operations that are difficult to recover. An authority grant cannot override this group; use a safer, explicitly scoped alternative.

Examples:

```bash
rm -fr /
rm -r -f $HOME
git reset --hard HEAD
git clean -f -d
mkfs ...
diskutil erase ...
dd if=...
```

Flow:

```text
Codex attempts a categorically blocked command
                    |
                    v
          PreToolUse denies it
                    |
                    v
       Command never reaches the shell
```

### Protected commands requiring an exact grant

The hook protects commands associated with push, release, publication, deploy, production, or destructive mutations. Current examples include:

- `git push`;
- `gh release`, `npm publish`, `cargo publish`, and `twine upload`;
- `vercel --prod`, deployment commands, `gcloud ... deploy`, and `kubectl apply`;
- commands marked as production operations;
- `terraform destroy`, `kubectl delete`, `DROP DATABASE`, `DROP TABLE`, and `DELETE FROM`.

Before one of these commands can run, `.tuxedo/authority.json` must contain a grant with:

- the matching operation name;
- the SHA-256 hash of the complete command string Codex is about to execute.

For example, this command:

```bash
git push origin feature
```

has this SHA-256 hash:

```text
07ee9c93ab3fbe9709f0dbfb8aa3497c3163e562dad3d9607d27491da47f90d2
```

Its grant is:

```json
{
  "version": 1,
  "grants": [
    {
      "operation": "push",
      "command_sha256": "07ee9c93ab3fbe9709f0dbfb8aa3497c3163e562dad3d9607d27491da47f90d2",
      "note": "Push the reviewed feature branch."
    }
  ]
}
```

Calculate a command hash without executing the command:

```bash
python3 -c 'import hashlib; command="git push origin feature"; print(hashlib.sha256(command.encode()).hexdigest())'
```

The match is exact. Whitespace, arguments, targets, or chained commands change the hash and invalidate the grant. A compound command that matches multiple protected operations needs a grant for every matching operation, all using the hash of the complete compound command.

Flow without a matching grant:

```text
Codex attempts: git push origin feature
                    |
                    v
      .tuxedo/authority.json absent,
       malformed, or hash does not match
                    |
                    v
          PreToolUse denies it
                    |
                    v
       Command never reaches the shell
```

Flow with the matching grant:

```text
Codex attempts: git push origin feature
                    |
                    v
     Matching push grant and exact hash
                    |
                    v
          PreToolUse allows it
                    |
                    v
              Command runs
```

The hook proves only that a matching local grant exists. It cannot prove who created the file or whether that person had organizational authority.

## Evidence receipts

Receipts are optional. They are inactive when the project has no `.tuxedo/policy.json`.

To opt in, copy `templates/policy/policy.json` to `.tuxedo/policy.json`. The default template requires receipts before both `git commit` and `Stop`:

```json
{
  "version": 1,
  "require_receipts_on": ["commit", "stop"],
  "receipt_path": ".tuxedo/receipts.json"
}
```

The receipt points to the active specification, behavior matrix, and evidence record. It also stores the expected SHA-256 hash of each artifact:

```json
{
  "version": 1,
  "spec": "specs/0007-example/spec.md",
  "behavior_matrix": "specs/0007-example/behavior-matrix.md",
  "evidence": "specs/0007-example/evidence.md",
  "artifact_hashes": {
    "specs/0007-example/spec.md": "<current SHA-256>",
    "specs/0007-example/behavior-matrix.md": "<current SHA-256>",
    "specs/0007-example/evidence.md": "<current SHA-256>"
  }
}
```

Generate a file hash with:

```bash
shasum -a 256 specs/0007-example/spec.md
```

### Commit example

Assume the project requires a receipt on `commit`.

```text
Codex attempts: git commit -m "feat: add example"
                    |
                    v
      PreToolUse reads the policy and receipt
                    |
          +---------+---------+
          |                   |
          v                   v
 All required files      Receipt missing,
 exist and hashes        malformed, incomplete,
 still match             or hash is stale
          |                   |
          v                   v
 Commit runs          Commit is denied
```

### Completion example

Assume the project requires a receipt on `stop`. Codex ran tests and created a receipt, but someone then edited the spec. Its current hash no longer matches the recorded hash.

```text
Codex attempts to finish the turn
                    |
                    v
          Stop validates receipts
                    |
                    v
       Spec hash differs from receipt
                    |
                    v
   Stop asks Codex to continue and refresh
         the evidence before finishing
```

If the project requires only commit receipts, use `"require_receipts_on": ["commit"]`. If it requires only completion receipts, use `["stop"]`. Removing `.tuxedo/policy.json` disables receipt checks but does not disable command protection.

## Malformed hook input

If Codex invokes a protected hook with missing or malformed JSON, an invalid working directory, or an unexpected event shape, Tuxedo denies the operation instead of guessing. This fail-safe behavior is covered by deterministic fixtures.

## What the hooks do not enforce

The hooks do not establish:

- the semantic quality or completeness of a spec, test, review, or architecture;
- that a receipt contains good evidence rather than merely current files;
- that an authority grant was created by a human or approved by an organization;
- coverage of aliases, arbitrary wrapper binaries, hosted tools, unsupported tool paths, or future schema changes;
- reversal of an effect that already happened;
- completion enforcement outside a trusted and enabled Codex hook runtime.

`Stop` can request another continuation; it cannot prove that the final result is correct. Projects that require centrally enforced organizational policy need managed Codex policy or another control outside this plugin.

## Privacy and execution properties

The hook runs locally and deterministically. It performs no network requests. It reads only its JSON event, the opt-in policy/grant/receipt files, and the bytes of explicitly named receipt artifacts to calculate hashes. It never emits artifact contents, prompts, environment variables, or secrets.
