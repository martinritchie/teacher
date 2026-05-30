# BrierLM: Unbiased Estimation

## Original Text

Specifically, the uncertainty term, $\sum_x P(x)^2$, can be interpreted as the collision probability of two independent samples. Therefore, its unbiased estimator is simply the indicator function $I\{x_1 = x_2\}$, where $x_1, x_2 \sim P$. Similarly, the accuracy term $P(y)$ can be estimated by $I\{x = y\}$ using a single sample $x \sim P$.

Combining these, we construct a practical, unbiased estimator for the Brier score using two samples drawn from the model:

$$\text{Brier}(P, y) \approx I\{x_1 = y\} + I\{x_2 = y\} - I\{x_1 = x_2\}, \quad x_1, x_2 \sim P$$

This estimator enables a likelihood-free evaluation of CALM's predictive capabilities. A straightforward approach is to assess next-token prediction performance in a teacher-forcing setting. However, such an evaluation is insufficient as it ignores the generation quality of the remaining $K - 1$ tokens.

To address this limitation, we further introduce Brier-n, a metric that computes the Brier score over entire n-grams. In this formulation, the indicator functions of the estimator treat the n-gram as a single, atomic outcome. Finally, following the convention of established n-gram-based metrics like BLEU, we define our composite metric, BrierLM (Brier for Language Modeling), as the geometric mean of Brier-n scores for $n = 1$ to 4, which we then scale by 100:

$$\text{BrierLM} = 100 \cdot \left(\prod_{n=1}^{4} \text{Brier-n}\right)^{0.25}$$


## Teacher

The key insight enabling likelihood-free estimation lies in reinterpreting the Brier score's two terms probabilistically.

Consider the uncertainty term—the sum of squared probabilities across all outcomes. This quantity has a beautiful interpretation: it equals the collision probability, the chance that two independent samples from the distribution happen to be identical. `<break time="0.8s" />` Therefore, an unbiased estimator is simply the indicator function that checks whether two independent samples match. Draw two samples from P. If they're identical, the estimate is one; otherwise zero.

Similarly, the accuracy term—the probability assigned to the ground truth outcome—can be estimated by drawing a single sample and checking whether it matches the ground truth.

Combining these, the authors construct a practical, unbiased estimator for the Brier score using just two samples drawn from the model. `<break time="0.6s" />` The estimator checks three things. `<break time="0.4s" />` First: does the first sample match the ground truth? `<break time="0.3s" />` Second: does the second sample match the ground truth? `<break time="0.3s" />` Third: do the two samples match each other? `<break time="0.5s" />` The first two contribute positively, rewarding accuracy. The third contributes negatively, penalizing low diversity.

`<break time="1.0s" />`

This estimator enables likelihood-free evaluation of the model's predictive capabilities. A straightforward approach would assess next-token prediction in a teacher-forcing setting. However, such evaluation is insufficient—it ignores the generation quality of the remaining K minus one tokens in each chunk.

To address this limitation, the authors introduce Brier-n, which computes the Brier score over entire n-grams. `<break time="0.5s" />` The indicator functions now treat each n-gram as a single atomic outcome. Finally, following the convention of established n-gram metrics like BLEU, the authors define their composite metric, BrierLM, as the geometric mean of Brier-n scores for n equals one through four, scaled by one hundred. This provides a comprehensive measure of generation quality across multiple granularities.