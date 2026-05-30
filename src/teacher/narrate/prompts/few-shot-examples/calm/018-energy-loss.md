# Energy Loss: Practical Implementation

## Original Text

To construct an unbiased Monte Carlo estimator, we draw $N$ candidate samples, $\{\tilde{z}_{i,1}, \ldots, \tilde{z}_{i,N}\}$, from the generative head at each step $i$. Furthermore, we leverage a unique property of our setup: our autoencoder does not map a token chunk to a fixed point, but rather to a conditional Gaussian posterior $z_i \sim q(\cdot|x_{(i-1)K+1:iK})$.

Relying on a single sample $z_i$ as ground-truth can introduce high variance into the energy loss. To mitigate this and stabilize training, we draw $M$ target samples, $\{z_{i,1}, \ldots, z_{i,M}\}$, from this posterior.

Combining these sample sets, the final energy loss is formulated as:

$$\mathcal{L}_{energy} = \sum_{i=1}^{L} \left(\frac{2}{NM}\sum_{n=1}^{N}\sum_{m=1}^{M}\|z_{i,m} - \tilde{z}_{i,n}\| - \frac{1}{N(N-1)}\sum_{n \neq k}\|\tilde{z}_{i,n} - \tilde{z}_{i,k}\|\right)$$

In practice, we set $N = 8$ and $M = 100$. The number of model samples $N$ directly scales the training cost, as each sample requires an evaluation of the generative head; we therefore use a small $N$ to maintain high training efficiency. The overhead of drawing target vectors from a known Gaussian posterior is almost negligible, which allows us to use a large $M$ to reduce the variance of loss.

## Teacher

While the expectations in the Energy Score formula make it intractable to compute exactly, the authors construct an unbiased Monte Carlo estimator to serve as their practical loss function.

At each step, the authors draw N candidate samples from the generative head—these are the model's predictions. But there's a subtle advantage in their setup: the autoencoder doesn't map a token chunk to a fixed point, but rather to a conditional Gaussian posterior. Relying on a single sample as ground truth would introduce high variance into the energy loss. To stabilize training, the authors draw M target samples from this posterior.

The final energy loss combines these sample sets. The fidelity term computes distances between the N predicted vectors and the M ground truth vectors sampled from the autoencoder's posterior. The diversity term measures distances among the N predictions themselves.

In practice, the authors set N to 8 and M to 100. The number of model samples N directly scales training cost, since each sample requires evaluating the generative head—so the authors use a small N to maintain efficiency. Drawing target vectors from a known Gaussian posterior is nearly free, allowing a large M to reduce variance.

A key advantage of this likelihood-free objective: it only requires the ability to draw samples from the generative head, placing minimal constraints on its architecture. This enables the simple, efficient designs the authors explore next.