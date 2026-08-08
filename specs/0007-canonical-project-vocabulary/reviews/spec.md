# SPEC-0007 spec review

Date: 2026-08-08

## Review boundary

Reviewed the user request and annotation, complete SPEC-0007, existing glossary,
package/distribution boundaries, and task-authority model without using tests,
the candidate diff, or implementation wording as justification.

## Spec

- No findings. `user-authorized` follows the person who controls task scope and
  remains correct whether or not that person is a developer or maintainer.
- Product identity, development tooling, repository content, task authority,
  and stewardship are materially distinct contexts and have explicit terms.

## Standards

- The specification preserves package isolation and the historical-record
  boundary rather than requiring a misleading global replacement.
- The private Node manifest and plugin manifest may both use `tuxedo`; they are
  separate package systems and no Node publication is authorized.

## Risk

- The change is medium because it touches authority language and multiple
  public/repository contract surfaces, despite no runtime behavior change.
- The principal risk is semantic overreach: replacing a legitimate actor or
  historical statement. TV-005 makes that a reviewable exclusion.
