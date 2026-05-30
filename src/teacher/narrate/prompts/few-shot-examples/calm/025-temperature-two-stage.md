# Two-Stage Rejection Sampling for Arbitrary Temperature

To generalize this approach for any arbitrary temperature $T \in (0, 1)$, we decompose the exponent $1/T$ into its integer part, $n = \lfloor 1/T \rfloor$, and fractional part, $\alpha = 1/T - n$. This decomposition structures our algorithm as a two-stage rejection sampling process.

The first stage handles the integer component $n$ using the repetition-based scheme described above, producing a candidate sample $x^*$ only if $n$ independent draws are identical. The second stage, which handles the fractional exponent $\alpha$, requires a more subtle approach.

Here, we draw upon the theory of Bernoulli Factory to construct an iterative procedure that simulates a biased coin flip with a success probability of $P(x^*)^\alpha$. A sample is accepted only if it passes both stages; failure at any point triggers a restart of the entire process.

**Theorem 1** (Exactness): For an implicit discrete distribution $P(x)$ with sampler $S$ and a temperature $T \in (0, 1)$, the two-stage algorithm generates samples distributed as:

$$P_T(x) = \frac{P(x)^{1/T}}{Z_T}, \quad Z_T = \sum_x P(x)^{1/T}$$

This theorem guarantees that the algorithm produces exact samples from the desired temperature distribution, making it a theoretically principled approach to likelihood-free temperature sampling.
