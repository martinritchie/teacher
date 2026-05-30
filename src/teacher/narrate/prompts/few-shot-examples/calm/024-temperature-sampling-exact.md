# Likelihood-Free Temperature Sampling: Exact Algorithm

Controlled generation via temperature sampling is an indispensable feature of modern LLMs. Conventionally, this technique is implemented by rescaling pre-softmax logits, a mechanism that requires explicit access to the model's probability distribution. However, this approach is incompatible with our CALM framework, whose generative head is likelihood-free and provides only a sampler.

This presents a critical challenge: performing temperature sampling with only a black-box sampler. In this section, we address this challenge by developing an exact algorithm, grounded in the principles of rejection sampling, that provably achieves this goal.

The intuition for our algorithm stems from the relationship between repeated sampling and probability exponentiation. Consider the simple case where the temperature $T = 1/n$ for an integer $n$, which makes the target distribution $P_T(x) \propto P(x)^n$. The probability of drawing the exact same sample $x$ in $n$ independent trials from the sampler is also $P(x)^n$.

This motivates an elegant rejection sampling scheme: we draw $n$ samples and accept them if and only if all $n$ samples are identical. Otherwise, we reject the entire set and restart the process. The distribution of accepted samples is thus provably proportional to $P(x)^n$, providing a foundation for our general algorithm.
