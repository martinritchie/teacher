# Strictly Proper Scoring Rules

## Original Text

To meet the demand for a generative head capable of high-quality, single-step generation, we draw inspiration from Shao et al. (2024; 2025b), which frames the generative task as the optimization of strictly proper scoring rules.

Formally, a scoring rule $S(P, y)$ assigns a numerical score to a predictive distribution $P$ upon observing an outcome $y$, where higher scores are better. The quality of a forecast $P$ against the true data-generating distribution $Q$ is measured by its expected score:

$$S(P, Q) = \mathbb{E}_{y \sim Q}[S(P, y)]$$

A scoring rule is considered proper if the expected score is maximized when the predictive distribution $P$ matches the data distribution $Q$:

$$S(P, Q) \leq S(Q, Q) \quad \text{for all distributions } P$$

Furthermore, a scoring rule is strictly proper if equality holds only when $P = Q$, meaning that the optimal score can only be achieved by reporting the true distribution. The use of a strictly proper scoring rule as a training objective is therefore a powerful and principled approach for training our generative head, as maximizing the expected score is equivalent to driving the model's predictive distribution to match the true distribution.

## Teacher

To meet the demand for single-step generation, the authors draw on the theory of strictly proper scoring rules—a principled framework from statistics that generalizes maximum likelihood estimation to settings where likelihood is intractable.

Here's the core idea. A scoring rule assigns a numerical score to a predictive distribution upon observing an outcome, where higher scores are better. Think of it as a way to grade a forecast. The quality of a forecast P against the true data-generating distribution Q is measured by its expected score—the average score you'd get if you repeatedly drew outcomes from Q and scored your forecast P.

A scoring rule is considered proper if the expected score is maximized when the predictive distribution P matches the data distribution Q. In other words, honesty is rewarded: your best strategy is to report your true beliefs, not some distorted version. A scoring rule is strictly proper if this maximum can only be achieved by perfect honesty—when P equals Q exactly.

The authors leverage this theoretical framework as their training objective. Using a strictly proper scoring rule to train the generative head is both powerful and principled: maximizing the expected score drives the model's predictive distribution to match the true distribution. This is a direct generalization of maximum likelihood estimation, where negative log-likelihood is a special case corresponding to the logarithmic score.

The key advantage for the authors' application is that while likelihood is intractable in continuous space, the theory of scoring rules provides a rich toolkit of alternatives that remain tractable. The authors specifically adopt the Energy Score, which they implement as a practical loss function in the next section.