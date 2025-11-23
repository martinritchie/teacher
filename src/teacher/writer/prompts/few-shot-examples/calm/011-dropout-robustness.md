# Dropout for Enhanced Robustness

## Original Text

Beyond structuring the latent space with variational methods, we further enhance its robustness by injecting noise during training using two complementary forms of dropout.

First, we apply dropout with a rate of $p = 0.15$ to the latent vector $z$ before it is passed to the decoder. This forces the autoencoder to learn a redundant representation, making it robust to minor prediction errors from the downstream generative model.

Second, we apply dropout to input tokens by randomly masking a fraction ($p = 0.15$) of tokens. Analogous to the Continuous Bag-of-Words (CBOW) method, this compels the autoencoder to infer masked tokens from their context, thereby enriching the latent vector with the chunk's semantic context rather than just performing a simple token-index compression.

Crucially, these dropout techniques are employed exclusively during the autoencoder's training phase to build a robust latent representation; they are disabled during the subsequent training and inference of the continuous language model.

## Teacher

Beyond structuring the latent space with variational methods, the authors further enhance its robustness by injecting noise during training through two complementary forms of dropout.

First, the authors apply dropout with a 15 percent rate to the latent vector before it's passed to the decoder. This forces the autoencoder to learn a redundant representation—if some latent dimensions might be randomly dropped, the remaining ones must carry enough information to reconstruct the input. This directly prepares the representation to handle the inevitable prediction errors from the downstream generative model.

Second, the authors apply dropout to the input tokens themselves, randomly masking 15 percent of them. This approach parallels the Continuous Bag-of-Words method: the autoencoder must infer the masked tokens from their context. Rather than simply compressing token indices, the latent vector becomes enriched with semantic understanding of the chunk's contextual meaning.

Crucially, the authors employ these dropout techniques only during autoencoder training to build robustness into the learned representation. They disable both forms of dropout during the subsequent training and inference of the continuous language model.

The result is a powerful, robust autoencoder. For a chunk of four tokens, the authors use a 128-dimensional latent vector. The learned standard deviations converge to about 0.3, meaning sampling introduces substantial Gaussian noise. Yet despite this significant perturbation, the decoder maintains token-level accuracy exceeding 99.9 percent. This representation—combining high fidelity with high robustness—provides a solid foundation for the subsequent continuous autoregressive language model.