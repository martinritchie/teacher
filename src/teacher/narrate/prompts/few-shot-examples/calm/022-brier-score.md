# BrierLM: Brier Score for Language Modeling

## Original Text

For a principled and likelihood-free evaluation, we turn to the Brier score, a classic strictly proper scoring rule now widely used to assess the calibration of modern neural networks. For a predictive distribution $P$ and a ground-truth outcome $y$, the Brier score is defined as:

$$\text{Brier}(P, y) = 2P(y) - \sum_{x} P(x)^2$$

Unlike the raw likelihood $P(y)$, which solely measures accuracy, the Brier score incorporates an additional term, $\sum_x P(x)^2$, to quantify predictive uncertainty. This structure balances two competing objectives, which ultimately rewards a well-calibrated prediction.

This property is revealed by the following decomposition of the expected Brier score:

$$\mathbb{E}_{y \sim Q}[\text{Brier}(P, y)] = -\sum_{x}(P(x) - Q(x))^2 + \sum_{x}Q(x)^2$$

The first term is squared error (minimized at $P = Q$), and the second term is data variance (constant).

While the Brier score is theoretically sound, its direct computation remains intractable for CALM, as it requires knowledge of the full predictive distribution $P$. We find, however, that an unbiased Monte Carlo estimator for the Brier score can be constructed in an entirely likelihood-free manner, using only samples drawn from the model.

## Teacher

For principled, likelihood-free evaluation, the authors turn to the Brier score — a classic strictly proper scoring rule now widely used to assess calibration in modern neural networks.

The Brier score has an elegant structure. <break time="0.5s" /> For a predictive distribution P and a ground-truth outcome y, it balances two terms. <break time="0.4s" /> The first term rewards accuracy: twice the probability assigned to the correct outcome. <break time="0.3s" /> The second term penalizes overconfidence: the sum of squared probabilities across all possible outcomes.

Unlike raw likelihood, which solely measures how much probability mass lands on the correct answer, the Brier score incorporates predictive uncertainty. <break time="0.5s" /> A model that hedges appropriately — spreading probability across plausible outcomes rather than overcommitting to one — receives credit for this calibration. This structure rewards predictions that are both accurate and well-calibrated.

The theoretical soundness of the Brier score is revealed by decomposing its expected value. <break time="0.5s" /> When you take the expectation over ground-truth outcomes drawn from the true distribution Q, the expected Brier score decomposes into two terms. <break time="0.4s" /> The first is negative squared error between P and Q, which is uniquely minimized when the distributions match exactly. <break time="0.3s" /> The second is the variance of the data distribution itself — a constant that doesn't depend on the model's predictions. <break time="0.5s" /> This decomposition confirms the Brier score satisfies the authors' criterion: it's uniquely optimized when the model recovers the true distribution.

However, a challenge remains. <break time="0.6s" /> Direct computation of the Brier score requires knowledge of the full predictive distribution P — something the authors' implicit generative model cannot provide. <break time="0.5s" /> The authors' key insight is that an unbiased Monte Carlo estimator for the Brier score can be constructed in an entirely likelihood-free manner, using only samples drawn from the model.