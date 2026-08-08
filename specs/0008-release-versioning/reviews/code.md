# SPEC-0008 code and security review

## Review boundary

This phase reviewed the complete task-owned diff with SPEC-0008, its matrix,
the reviewed tests, local command evidence, action pins, and current GitHub
settings. The concurrent unrelated `AGENTS.md` edit was inspected only to prove
that it is outside the candidate and is not included below.

## Spec

- Root and plugin versions now agree at `0.1.0`; one manifest/config drives the
  root Release Please package and plugin JSON version.
- Stable install/upgrade documentation uses immutable tags and explains that
  `tuxedo@tuxedo` is identity, not version syntax.
- The initial changelog and release guide define the pre-1.0 increment policy,
  explicit merge/publication boundary, immutable rollback path, and no-npm
  boundary.
- CI contains every required deterministic check and leaves provider/model
  evaluation outside automatic workflows.

## Standards

- All external Actions are pinned by full commit SHA. The official validators
  are fetched from the immutable OpenAI Codex `rust-v0.146.0` commit matching
  the repository's exact Codex SDK/CLI family.
- Pull-request CI has only `contents: read`; checkout never persists its token.
  The release mutation job has only its documented write scopes and never
  checks out or executes repository content.
- Generated Release PR validation executes with `contents: read`. The separate
  status job has only `statuses: write`, performs no checkout, and reports the
  result for the API-resolved and locally confirmed head SHA.
- No dependency, installed-plugin runtime, npm publication, cache, provider
  credential, deployment, or auto-merge was added.

## Risk

- Threat boundary: untrusted pull-request content may execute in validation but
  receives no write/publication credential. It may observe a read-only token;
  the repository is public and checkout persistence is disabled.
- Release Please retains repository write authority, so compromise of the
  pinned action remains a supply-chain risk. Full-SHA pinning, no repository
  checkout, least-privilege scopes, protected `main`, and human Release PR merge
  reduce but do not eliminate it.
- The `Validate` status bridge is intentionally narrow but still depends on
  GitHub's required-status semantics. PR #2 demonstrated its failure path, PR
  #3 and protected `main` demonstrated its successful path, and the protection
  API resolves `Validate` to GitHub Actions app `15368`.
- The first post-bootstrap `feat` remains the empirical proof that Release
  Please proposes `0.2.0`; the official schema and configuration establish the
  current deterministic contract but not a future GitHub service outcome.
- The first Release Please run did propose `0.2.0`, but it incorrectly included
  pre-bootstrap history. PR #2 was blocked by the status bridge and closed;
  top-level `bootstrap-sha` now excludes that history until `v0.1.0` exists.
- Checkout/setup-node now use pinned v5 commits, and unused setup-node/UV caches
  are explicitly disabled. PR #3's fail-first run caught the setup-node cache
  default before the final run passed. A non-blocking `punycode` deprecation
  remains inside the Action runtime and produced no GitHub annotation.

No blocking code, standards, or security finding remains. RV-005, RV-007,
RV-008, and RV-009 are satisfied. The first genuinely post-bootstrap `feat`
remains future empirical evidence for RV-010.
