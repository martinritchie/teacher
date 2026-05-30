# Expected Sampling Cost Analysis

While the exact algorithm provides a principled solution for likelihood-free temperature sampling, its practical viability hinges on its computational efficiency. A central concern is the expected number of samples it requires, as each sampler call involves a forward pass through the generative head and autoencoder.

**Theorem 2** (Expected Cost): The expected number of calls to the base sampler $S$, denoted $\mathbb{E}[N_{total}]$, required to generate one sample using the two-stage algorithm is:

$$\mathbb{E}[N_{total}] = n + \mathbb{I}(\alpha > 0)\frac{\sum_x P(x)^{1/T - 1}}{Z_T}$$

where $Z_T = \sum_x P(x)^{1/T}$, $n = \lfloor 1/T \rfloor$, $\alpha = 1/T - n$, and $\mathbb{I}(\cdot)$ is the indicator function.

**Corollary 2.1** (Cost Bounds): The expected number of sampler calls is bounded by:

$$\mathbb{E}[N_{total}] \leq \begin{cases}
\frac{1 + n}{Z_T} & \text{if } 0 < T \leq 0.5\\
\frac{1 + |X|^{2-1/T}}{Z_T} & \text{if } 0.5 < T < 1
\end{cases}$$

These results highlight that the algorithm's practicality is highly sensitive to temperature $T$. A potential limitation first emerges for $T \to 1$, as the cost can scale up to the size of sample space $|X| = |V|^K$. It is therefore advisable to avoid using temperatures in this high-temperature regime to prevent a potential computational bottleneck.
