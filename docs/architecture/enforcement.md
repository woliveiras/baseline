# Enforcement boundaries

Tuxedo separates two kinds of executable reinforcement:

1. Codex Rules handle command authority and command-level safety.
2. Tuxedo hooks validate the mechanical integrity of the spec-driven workflow.

Neither mechanism decides whether a specification, test, architecture, or documentation change is semantically good.

The maintainer-only Promptfoo evaluation boundary is documented separately in
[the evaluation architecture](evaluations.md) and [ADR 0001](../decisions/0001-use-promptfoo-as-evaluation-orchestrator.md).
Promptfoo does not replace these rules, hooks, or deterministic verifiers.

## Codex Rules

Tuxedo ships `templates/codex/tuxedo.rules` as an opt-in project template. Copy it to `.codex/rules/tuxedo.rules` in a trusted project and restart Codex.

For the exact, standard direct command forms listed in the template, it:

- forbids a narrow set of broad recursive deletions;
- prompts before push, destructive Git cleanup, release, package publication, deployment, cluster mutation, and infrastructure mutation;
- includes `match` and `not_match` examples that Codex validates when loading the rules.

Codex Rules evaluate command arguments and use Codex's native shell handling. They replace Tuxedo's former regular-expression command classifier and exact-command authority files. The approval shown by Codex is the authority boundary; Tuxedo does not duplicate it in `.tuxedo/authority.json`.

Rules are an experimental Codex feature. The included policies use exact argument prefixes. An absolute executable such as `/usr/bin/git`, a wrapper such as `env git`, or a global option inserted before the matched subcommand such as `git -C project push` does not match the corresponding template rule. Shell scripts with substitutions, redirections, assignments, wildcards, or control flow may also be treated conservatively as one shell invocation instead of being decomposed. The sandbox, project trust, approval configuration, and organizational policy remain authoritative for forms outside the template.

## Workflow hooks

The plugin loads `hooks/hooks.json` after the user reviews and trusts its current definition.

| Event | Mechanical gate |
| --- | --- |
| `PreToolUse` for `Bash` | Before a direct `git commit ...`, validate the opt-in completion receipt. Other commands pass through unchanged. |
| `Stop` | Before Codex finishes a turn, validate the opt-in completion receipt. |

A direct commit means the command tokenizes with `git` as the executable and `commit` as its first argument. The hook deliberately does not parse compound shell programs. The `Stop` gate remains the complete end-of-turn check.

Hooks are inactive for a project without `.tuxedo/policy.json`. To opt in, copy `templates/policy/policy.json` to that path.

## Receipt chain

The version 2 completion receipt binds the current artifacts into this dependency chain:

```text
spec
  -> spec review
  -> behavior/oracle matrix
  -> test tree
  -> test review
  -> implementation tree + evidence + documentation decision
  -> code review
  -> commit / Stop gate
```

The receipt names:

- the spec, behavior matrix, and evidence record;
- complete SHA-256 maps for the configured test and implementation scopes;
- structured fail-first and passing records tied to the current test-tree digest, with non-empty commands and observations;
- an explicit documentation decision with rationale and optional hashed artifacts;
- spec, test, and code review receipts;
- hashes for all canonical and review artifacts.

The default policy requires non-empty test and implementation trees. Its `tree_scopes` are an illustrative conventional layout: maintainers must adapt the include and exclude globs to the project's real source and test layout. Each receipt tree must then contain exactly every current file in its configured scope; omitted files and files borrowed from another scope fail the gate. A spec-only or documentation-only workflow can set `required_trees` to an empty list or require only the applicable tree without weakening the other checks.

### Three review receipts

Start from the assets in `templates/review/` or the self-contained assets bundled with the `verify` skill.

- Spec review receives the spec, declares tests and implementation unexposed, and records the resulting matrix hash.
- Test review receives the approved spec, matrix, spec-review receipt, test-tree digest, and fail-first record digest while declaring the implementation unexposed.
- Code review receives the upstream artifacts, implementation and test-tree digests, complete test-evidence digest, fresh evidence, and documentation digest.

Set a review receipt to `approved` only after its actionable findings are reconciled. A downstream review includes the hash of its upstream review, so changing an earlier artifact invalidates the final gate.

### Hashes and digests

Each file hash is the lowercase SHA-256 of its bytes:

```bash
shasum -a 256 path/to/file
```

A tree digest is the SHA-256 of its path-to-hash object serialized as minified JSON with sorted keys. This command prints the digest of a saved hash map without reading source contents into model context:

```bash
python3 -c 'import hashlib,json,sys; value=json.load(open(sys.argv[1])); print(hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",", ":")).encode()).hexdigest())' tree-hashes.json
```

The documentation digest uses the same canonical serialization over:

```json
{
  "decision": "required or not-required",
  "rationale": "the recorded rationale",
  "artifact_hashes": {
    "path/from/documentation.artifacts": "its receipt hash"
  }
}
```

The fail-first record and complete `test_evidence` object use the same canonical serialization. Both the fail-first and passing records must name the digest of the current configured test tree. Their commands and observations must be non-empty. For a workflow with no test scope, `test_evidence` may be `null`.

The hook recalculates every file hash, both tree digests, the structured test-evidence digests, the documentation digest, and the expected inputs of all three reviews.

## What the gates establish

The hooks establish that:

- required artifacts exist inside the project;
- their current bytes match the receipt;
- required test and implementation trees are non-empty and exactly cover their configured scopes;
- fail-first and passing records refer to the current test tree and contain commands and observations;
- documentation impact was explicitly decided;
- required documentation artifacts are hashed;
- review receipts declare the expected context separation;
- every downstream review references the current upstream digests.

The dependency chain reinforces the artifacts Tuxedo requires: spec and behavior matrix, fail-first and passing test evidence tied to the current test tree, test review before final code review, and an explicit documentation decision. It cannot prove that the recorded commands really ran or establish wall-clock ordering: an agent could create a dishonest receipt later. A policy with incomplete `tree_scopes` can also omit files that its globs never select. The gate cannot prove that a reviewer actually avoided implementation exposure or that an oracle captures the right behavior. Those remain skill, review, policy-configuration, and evaluation concerns.

## Malformed inputs and privacy

Malformed hook input, escaping artifact paths, stale hashes, incomplete reviews, or invalid documentation decisions fail closed when the corresponding gate is active.

The hook runs locally, performs no network requests, and reads only its event, policy, receipt, configured tree scopes, and named artifacts. It emits no artifact contents, prompts, environment variables, transcripts, or secrets.
