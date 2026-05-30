# Batch Approximation for Low-Temperature Regime

The practical limitations of the exact algorithm become most pronounced in the low-temperature regime, where the requirement of drawing $n = \lfloor 1/T \rfloor$ identical samples leads to an extremely high rejection rate that results in poor sample utilization.

To address this, we propose an efficient approximate algorithm tailored for low temperatures of the form $T = 1/n$. The key insight is to shift from a single, high-risk trial to a combinatorial search within a large batch of $N$ samples ($N \gg n$).

This shift allows a single batch to constitute $\binom{N}{n}$ distinct candidates, which dramatically improves sample utilization and increases the probability of finding a successful match in a single round. For example, to sample at $T = 0.5$ ($n = 2$), we might draw a batch of $N = 10$ samples. Here, sample $A$ appears three times, and sample $B$ appears twice. The algorithm then counts the number of successful n-tuple candidates within this batch. For sample $A$, there are $\binom{3}{2} = 3$ successful candidates. For sample $B$, there is only $\binom{2}{2} = 1$ successful candidate. The output is sampled from the set of valid candidates $\{A, B\}$ according to their weighted probabilities.

**Theorem 3** (Asymptotic Unbiasedness): The batch approximation algorithm is asymptotically unbiased: $\lim_{N \to \infty} P_{alg}(x; N) = P_T(x)$.

This property of consistency establishes the algorithm as a principled approximation where the batch size $N$ serves as a practical lever for the trade-off between efficiency and accuracy.
