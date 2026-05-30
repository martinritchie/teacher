# Main Results: Performance-Compute Trade-off

We present the primary results comparing standard Transformer baselines with CALM (K=4). The results demonstrate CALM establishes a more efficient performance-compute frontier for language modeling.

By increasing semantic bandwidth per autoregressive step, CALM allows larger models with fewer FLOPs for training and inference.

**Key Finding**: CALM-M (371M) achieves comparable BrierLM to Transformer-S (281M) with 44% fewer training FLOPs and 34% fewer inference FLOPs.

CALM benefits from scaling just as effectively as Transformers. The semantic bandwidth $K$ serves as a new lever for performance-compute optimization. CALM-L with $K = 1$ is at disadvantage; advantages emerge as $K$ increases. From $K = 1$ to $K = 2$, cost nearly halves with marginal performance drop. At $K = 4$, CALM surpasses the discrete baseline.

This validates our central hypothesis: scaling semantic bandwidth of each generative step provides a highly effective axis for optimizing performance-compute trade-off.
