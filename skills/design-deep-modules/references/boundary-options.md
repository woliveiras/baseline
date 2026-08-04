# Boundary options

Hold behavior, invariants, compatibility, failure cases, and test needs constant while comparing interfaces.

| Option | Caller knowledge | Hidden decisions | Dependency placement | Seam | Locality/deletion | Migration/reversal | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |

For each dependency, record responsibility, lifecycle ownership, volatility, build-time and runtime direction, and what callers must order, translate, retry, or clean up. Reject options using observed cost or violated constraints, not current folder layout. Replace private-structure tests only after boundary coverage demonstrates equivalent observable protection.
