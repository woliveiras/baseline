# Diagnostic escalation

Do not load this for an ordinary defect with a direct reproduction and causal repair. Escalate when the symptom cannot be reproduced reliably, the first discriminating probe falsifies the leading explanation, the failure depends on order or timing, or a previous repair did not fit the evidence.

1. Minimize the symptom while retaining the observable failing boundary. Record the smallest setup, action, expected signal, observed signal, and conditions that make it appear or disappear.
2. State competing hypotheses. For each, name a prediction and a falsifier before gathering more evidence. Rank by fit and impact, but run the cheapest probe that best separates them rather than the probe that merely confirms the favorite.
3. Compare good and bad conditions. Use a differential comparison across input, order, environment, version, state, or timing. Use `git bisect run` only when a deterministic script distinguishes commits and preserves the worktree.
4. Add the narrowest temporary instrumentation needed at the owning boundary. Bound volume and duration, exclude secrets and personal data, and label the removal condition. Do not treat logs as causal evidence when multiple hypotheses predict them.
5. Convert the supported cause into a fail-first regression at the closest observable seam. Apply the smallest causal repair, rerun the minimized reproduction and nearby suite, then remove temporary probes and confirm the regression still fails without the repair and passes with it.

Stop when evidence discriminates the cause, the repair fits it, regression and adjacent behavior pass, and instrumentation is gone. If the cause remains unresolved, report falsified hypotheses, the next discriminating probe, residual uncertainty, and the blast radius of further experimentation. Do not create a diagnostic artifact by default.
