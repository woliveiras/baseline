# Test provenance

- `spec-derived`: oracle follows an identifiable approved criterion or invariant.
- `independent`: oracle was derived without exposure to the new implementation.
- `implementation-aware`: author saw the new implementation before fixing the oracle.
- `external`: oracle comes from a protocol, standard, upstream contract, or verified reference system.
- `diagnostic-probe`: temporary observation used for reproduction or localization.

Record provenance per oracle, not per file. A test can contain multiple assertions with different provenance. Independence reduces shared-error risk but does not guarantee correctness.
