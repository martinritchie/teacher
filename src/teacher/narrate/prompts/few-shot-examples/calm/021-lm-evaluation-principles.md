# Principles of Language Model Evaluation

## Original Text

The CALM framework operates as an implicit generative model, whose predictive probability distribution is defined by its sampling process. Consequently, standard LM evaluation metrics like Perplexity, which are defined in terms of explicit likelihoods, can no longer be employed to measure model performance.

Furthermore, the energy loss used for training is itself unsuitable for evaluation, as its magnitude is subjective to the specific latent space shaped by the autoencoder. This necessitates the development of a model-agnostic evaluation metric, one that can faithfully assess language modeling capabilities in a principled, yet entirely likelihood-free, manner.

The goal of a evaluation metric is to quantify the divergence between the model's predictive distribution, $P$, and the true data distribution, $Q$. This principle is formalized by the property that the metric is uniquely optimized when the model accurately recovers the data distribution ($P = Q$). This ensures the evaluation is fair and cannot be hacked by a model that systematically distorts its predictions.

Perplexity is grounded in the expected negative log-likelihood, which can be decomposed into the sum of the KL divergence and data entropy, establishing it as a theoretically sound measure.

## Teacher

The authors now turn to a fundamental challenge: how do you evaluate a model that cannot compute likelihoods? <break time="1.0s" />

The continuous language model operates as an implicit generative model—its predictive distribution is defined entirely by its sampling process, not by an explicit probability density function. This means standard evaluation metrics like perplexity, which require explicit likelihoods, simply cannot be applied. <break time="0.8s" />

Furthermore, the energy loss used for training is unsuitable for evaluation. Its magnitude depends on the specific geometry of the latent space shaped by the autoencoder, making comparisons across different models or architectures meaningless. The authors need a model-agnostic evaluation metric—one that assesses language modeling capability in a principled, likelihood-free manner. <break time="1.0s" />

What makes an evaluation metric principled? <break time="1.0s" /> The authors articulate a clear goal: the metric should quantify the divergence between the model's predictive distribution P and the true data distribution Q. This is formalized by requiring that the metric is uniquely optimized when the model accurately recovers the data distribution—when P equals Q. This property ensures fair evaluation that cannot be gamed by a model that systematically distorts its predictions. <break time="0.8s" />

Perplexity satisfies this criterion through its connection to information theory. Expected negative log-likelihood decomposes into the sum of K L divergence between the true and predicted distributions, plus the entropy of the data itself. <break time="0.5s" /> Since K L divergence is minimized at zero only when the distributions match, perplexity provides a theoretically grounded measure. <break time="0.6s" /> The authors seek an analogous foundation for their likelihood-free setting.