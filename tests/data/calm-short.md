# CONTINUOUS AUTOREGRESSIVE LANGUAGE MODELS

## ABSTRACT

The efficiency of large language models (LLMs) is fundamentally limited by their sequential, token-by-token generation process. We argue that overcoming this bottleneck requires a new design axis for LLM scaling: increasing the semantic bandwidth of each generative step. To this end, we introduce Continuous Autoregressive Language Models (CALM), a paradigm shift from discrete next-token prediction to continuous next-vector prediction. CALM uses a high-fidelity autoencoder to compress a chunk of K tokens into a single continuous vector, from which the original tokens can be reconstructed with over 99.9% accuracy. This allows us to model language as a sequence of continuous vectors instead of discrete tokens, which reduces the number of generative steps by a factor of K. The paradigm shift necessitates a new modeling toolkit; therefore, we develop a comprehensive likelihood-free framework that enables robust training, evaluation, and controllable sampling in the continuous domain. Experiments show that CALM significantly improves the performance-compute trade-off, achieving the performance of strong discrete baselines at a significantly lower computational cost. More importantly, these findings establish next-vector prediction as a powerful and scalable pathway towards ultra-efficient language models.

## 1 INTRODUCTION

Large Language Models (LLMs) have revolutionized the field of artificial intelligence, demonstrating unprecedented capabilities in understanding, generating, and reasoning with human language (Achiam et al., 2023; Google, 2025; DeepSeek-AI, 2025). However, this remarkable success is shadowed by a critical challenge: their immense computational demands. The training and inference of state-of-the-art LLMs demand massive computational resources, leading to prohibitive expenses and significant environmental concerns (Strubell et al., 2019; Bender et al., 2021). At the heart of this inefficiency lies the foundational paradigm of these models: an autoregressive generation process that operates on a sequence of discrete tokens. Because the computational cost scales with the length of the sequence, generating long-form text or processing extensive contexts remains a fundamental bottleneck, limiting the scalability and accessibility of these powerful models.

## 2 AUTOENCODER

## 2.1 HIGH-FIDELITY RECONSTRUCTION

The foundational component of our CALM framework is an autoencoder tasked with learning a bijective mapping between a chunk of K discrete tokens and a continuous vector. Formally, we seek an encoder $f_{enc}:\mathcal{V}^{K}\to\mathbb{R}^{l}$ and a decoder $g_{dec}:\mathbb{R}^l\to \mathcal{V}^K$ , where V is the vocabulary, such that for a given token sequence $\mathbf{x}_{1:K} = (x_1, \dots, x_K)$ , the reconstruction $g_{dec}(f_{enc}(\mathbf{x}_{1:K}))$ closely approximates $\mathbf{X}_{1:K}$ . For simplicity and computational efficiency, we design our autoencoder to be context-free, meaning it processes each token chunk independently of its surrounding sequence. A context-aware autoencoder that also conditions on previous vector representations is a natural and promising next step, which we leave for future exploration.

## 8 CONCLUSION AND FUTURE WORK

In this work, we challenge the inefficient, token-by-token paradigm of LLMs by introducing Continuous Autoregressive Language Models (CALM), a framework that shifts generation from discrete tokens to a continuous vector space where a single vector represents K tokens. To support this approach, we develop a comprehensive likelihood-free toolkit: a robust and high-fidelity autoencoder, the energy loss for generative modeling, the BrierLM metric for LM evaluation, and a new suite of algorithms for temperature sampling. Empirical results show that CALM achieves a superior performance-compute trade-off, highlighting a new scaling axis for language modeling: scaling the semantic bandwidth of each generative step to push the performance-compute frontier of LLMs.

## REFERENCES

An experimental comparison of performance measures for classification. Pattern recognition letters, 30(1):27–38, 2009.

## A PROOF

## A.1 PROOF OF THEOREM 1

**Theorem 1.** For an implicit discrete distribution $P(x)$ with sampler S and a temperature $T\in (0,1)$ Algorithm 1 generates samples distributed as:
