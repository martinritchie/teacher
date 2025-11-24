# Energy Score and Loss Formulation

## Original Text

We build our training objective using the Energy Score, a strictly proper scoring rule that has proven effective across a range of generative applications. The energy score is entirely likelihood-free; rather than evaluating probability densities, it measures the alignment between the prediction and the observation via sample distances.

For a predictive distribution $P$ and a ground truth observation $y$, the energy score is defined as:

$$S(P, y) = \mathbb{E}_{x', x'' \sim P}[\|x' - x''\|^\alpha] - 2\mathbb{E}_{x \sim P}[\|x - y\|^\alpha]$$

where $x, x', x''$ are independent samples drawn from $P$. The score is strictly proper for any $\alpha \in (0, 2)$. Typically, $\alpha$ is set to 1.

The first term encourages diversity, penalizing the model for producing collapsed or overly confident predictions where all samples are identical. The second term encourages fidelity, driving the model's predictions to be close to the ground truth observation.

While the expectations in this equation make the energy score intractable to compute exactly, we can construct an unbiased Monte Carlo estimator to serve as a practical loss function.

## Teacher

The authors build their training objective using the Energy Score—a strictly proper scoring rule that has proven effective across generative applications. The Energy Score is entirely likelihood-free. Rather than evaluating probability densities, it measures alignment between prediction and observation through sample distances.

Here's the structure of the Energy Score. For a predictive distribution P and a ground truth observation y, the score has two terms. The first term measures the expected distance between pairs of independently sampled predictions—this is the diversity term. The second term measures the expected distance between predictions and the ground truth—this is the fidelity term, with a negative sign that makes it a penalty.

Let's understand what each term accomplishes. The diversity term encourages the model to produce varied samples. If the model collapses and always produces identical outputs, this distance is zero, contributing nothing to the score. If the model produces diverse samples, this distance is large. Since the authors will maximize this score during training—or equivalently, minimize the negative of it as a loss—this term pushes against collapsed, overconfident predictions.

The fidelity term drives predictions toward ground truth. Because of the negative sign, predictions close to the observation contribute a small penalty, while predictions far away contribute a large penalty. Maximizing the score therefore requires predictions that cluster near the ground truth.

The score is strictly proper for any alpha between zero and two, where alpha controls how distances are measured. The authors typically set alpha to one, giving them Euclidean distance.

While the expectations in the Energy Score formula make it intractable to compute exactly, the authors construct an unbiased Monte Carlo estimator to serve as their practical loss function. This is where the sampling strategy becomes critical.