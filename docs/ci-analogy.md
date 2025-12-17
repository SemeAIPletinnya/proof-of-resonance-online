# Proof-of-Resonance as a CI Analogy
Modern CI systems do not only test correctness.
They protect system integrity across change.

A test passing does not guarantee that:
- an API is still usable downstream
- a behavior is stable across versions
- a system remains coherent as a whole

This is why mature projects rely on guardrails such as:
- breaking-change detection
- regression checks
- downstream integration tests
In practice, CI answers a higher-level question:

"Did this change preserve the integrity of the system?"

Examples:
- Removing a public symbol → detected as a breaking change
- Changing behavior without test failure → caught by regression tests
- SDK change breaking an agent library → detected downstream
Reasoning systems face a similar problem.

A single correct answer does not guarantee:
- stable reasoning
- internal coherence
- robustness across prompts or formulations
Proof-of-Resonance (PoR) is an evaluation layer that measures
semantic stability across multiple independent samples.

Instead of asking:
"Is this answer correct?"

PoR asks:
"What remains stable when the answer is regenerated independently?"
CI (Software)                    PoR (Reasoning)
---------------------------------------------------------
Breaking change detection   →    Semantic instability detection
Regression tests            →    Cross-sample coherence checks
Downstream integration      →    Cross-context consistency
API integrity               →    Reasoning integrity
PoR is not:
- a training method
- a new model
- a replacement for accuracy or benchmarks
- not an AGI claim
PoR is:
- an evaluation guardrail
- complementary to existing metrics
- applicable across models
If CI protects systems from silent API breakage,
PoR protects reasoning from silent semantic collapse.
