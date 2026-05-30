# The Likelihood Intractability Challenge

## Original Text

The softmax function is not applicable over this uncountable set, rendering the explicit probability density $p(z_i | z_{<i})$ intractable. This introduces two critical challenges:

**Training Challenge**: The likelihood $p(z_i | z_{<i})$ becomes intractable, precluding the use of maximum likelihood estimation (i.e., minimizing cross-entropy loss) for training.

**Evaluation Challenge**: Standard evaluation metrics like Perplexity, which are derived directly from the model's likelihood, can no longer be computed to measure model performance.

We address both of these challenges in our framework. For the training problem, we introduce our approach to likelihood-free language modeling. For the evaluation problem, we propose a likelihood-free evaluation methodology that enables principled assessment of model performance without requiring explicit likelihoods.

## Teacher

Moving to continuous space fundamentally changes the mathematics of language modeling. In discrete space, the softmax function computes a probability distribution over a finite vocabulary, making the likelihood of each token explicit and tractable. But in continuous space, predicting a vector from an infinite set makes the probability density intractable to compute.

This intractability creates two critical challenges that shape the authors' entire approach.

First, the training challenge. Standard language models train by maximizing likelihood, which translates to minimizing cross-entropy loss. But if you cannot compute the likelihood of your predictions, you cannot use this objective. The authors need an entirely different training paradigm—one that doesn't require evaluating probability densities. This is where the Energy Score and proper scoring rules enter: they provide a principled, likelihood-free objective for training the generative head.

Second, the evaluation challenge. How do you measure model quality without likelihood? Standard metrics like perplexity derive directly from the model's probability assignments. Lower perplexity means the model assigns higher probability to the true next tokens. But in continuous space, you cannot compute these probabilities, so perplexity becomes undefined.

The authors address both challenges within their framework. For training, they've introduced the energy-based objective using proper scoring rules. For evaluation, they propose a likelihood-free methodology that assesses model performance through reconstruction accuracy—measuring how well the autoencoder can decode the predicted latent vectors back into the correct tokens. This approach sidesteps the need for explicit likelihoods while still providing a principled way to compare model quality.

Together, these solutions enable the authors to operate entirely in continuous space without sacrificing the ability to train effectively or evaluate performance rigorously.