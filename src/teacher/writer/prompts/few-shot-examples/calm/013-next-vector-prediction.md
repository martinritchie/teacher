# Next-Vector Prediction Framework

## Original Text

The autoencoder developed in the previous section establishes a robust and high-fidelity mapping between a chunk of $K$ discrete tokens and a single continuous vector, which allow us to reframe language modeling from a task of next-token prediction on discrete token sequences to next-vector prediction on continuous vector sequences.

Specifically, a sequence of $T$ tokens, $X = (x_1, \ldots, x_T)$, is first grouped into $L = T/K$ non-overlapping chunks. The encoder, $f_{enc}$, then transforms the original sequence into a new, more compact sequence of continuous vectors:

$$Z = (z_1, z_2, \ldots, z_L), \quad \text{where} \quad z_i = f_{enc}(x_{(i-1)K+1, \ldots, iK})$$

Consequently, the autoregressive objective evolves to predicting the next vector in the sequence:

$$p(Z) = \prod_{i=1}^{L} p(z_i | z_{<i})$$

While this autoregressive structure is preserved, the underlying mechanism for predicting the next element must be redesigned. Unlike standard language models, which rely on a softmax layer to compute a probability distribution over a finite vocabulary, our model must predict a vector within the infinite space $\mathbb{R}^l$.

## Teacher

The autoencoder established in the previous section creates a robust, high-fidelity mapping between a chunk of K discrete tokens and a single continuous vector. Building on this foundation, the authors reframe the fundamental task: instead of next-token prediction on discrete token sequences, they reformulate language modeling as next-vector prediction on continuous vector sequences.

Here's the transformation the authors implement. They group a sequence of T tokens into L non-overlapping chunks, where L equals T divided by K. The encoder then transforms this original sequence into a more compact sequence of continuous vectors, where each vector z represents the encoding of one chunk.

The autoregressive structure is preserved—the model still predicts the next element given all previous elements. But the mechanism must be fundamentally redesigned. Standard language models use a softmax layer to compute a probability distribution over a finite vocabulary. The authors' model must instead predict a vector within an infinite-dimensional continuous space.

This reformulation introduces two critical challenges. First, during training, the likelihood of each predicted vector becomes intractable, precluding maximum likelihood estimation and the standard cross-entropy loss. Second, evaluation metrics like perplexity, which derive directly from the model's likelihood, can no longer be computed.

The authors address both challenges with novel solutions. They introduce a likelihood-free approach to training based on strictly proper scoring rules, and they propose a likelihood-free evaluation methodology using reconstruction accuracy. Both represent significant departures from standard language modeling practice, but they enable effective prediction in continuous space—a key contribution of this work.