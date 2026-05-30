# Experiments: Settings and Configuration

**Datasets**: We train our models on the Pile uncopyrighted dataset. The raw text is processed with the Llama 3 tokenizer, resulting in a training set of $\sim$230B tokens. We evaluate model performance on the WikiText-103 benchmark.

**Model**: Our models are built upon a standard Transformer backbone. We adopt most of the architecture designs from the LLaMA family, including RMSNorm, SwiGLU activation, and rotary positional embeddings. We experiment with four scales:
- S (12 layers, hidden size=768, intermediate size=2048)
- M (16 layers, hidden size=1024, intermediate size=2752)
- L (16 layers, hidden size=1536, intermediate size=4096)
- XL (16 layers, hidden size=2560, intermediate size=6880)

**Training Details**: The training process for our CALM framework is two-staged. We first train a suite of autoencoders on a 15B token subset of the Pile to map token chunks of size $K \in \{1, 2, 4, 8\}$ into continuous vectors. These autoencoders use a hidden size of 512, a latent dimension of 32K, have approximately 75M parameters, and are trained for 30k steps with a batch size of 512k tokens.

Following this, the CALM models are trained on the remaining data for 250k steps with a batch size of 2 million tokens. The context length is set to 2048 steps; for CALM, this corresponds to 2048K tokens.
