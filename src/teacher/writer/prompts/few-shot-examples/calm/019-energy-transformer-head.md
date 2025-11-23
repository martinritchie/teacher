# Energy Transformer: Generative Head Architecture

## Original Text

We use a standard Transformer backbone, with modifications focused on the output-side generative head and the input-side adaptation.

**Energy-Based Generative Head**: The inputs to the generative head are twofold: the hidden state $h_{i-1}$ from the Transformer backbone, which provides the conditional context, and a random noise vector $\varepsilon \in \mathbb{R}^{d_{noise}}$, which provides the necessary stochasticity for sampling. Each dimension of $\varepsilon$ is drawn independently from a uniform distribution $U[-0.5, 0.5]$.

Both the hidden state $h_{i-1}$ and the noise vector $\varepsilon$ are projected by independent linear layers to match the head's internal dimension, which we set to match the Transformer's hidden dimension $d$.

The core of the generative head is a stack of $L$ residual MLP blocks that progressively refine the initial noise representation $\varepsilon_0 = \varepsilon$ into the final output vector. Each MLP block first fuses the current representation $\varepsilon_l$ with the hidden state via two linear layers. This is followed by a SwiGLU layer with an intermediate dimension of $d$. A residual connection then adds the block's input to its output. This process concludes with a final linear layer that projects the representation to the target dimension $l$, producing the output vector $z_i$.

A single MLP block contains approximately $6d^2$ parameters. We set the number of blocks to a quarter of the number of Transformer layers; the entire generative head therefore accounts for only about 10% of the total model parameters.


## Teacher

The authors implement their model using a standard Transformer backbone, with modifications focused on the generative head and input handling.

The generative head architecture reflects the authors' focus on efficiency combined with expressiveness. It receives two inputs. First, the hidden state from the Transformer backbone, which provides the conditional context for prediction. Second, a random noise vector that provides the stochasticity needed for sampling. The authors draw each dimension of this noise independently from a uniform distribution between negative 0.5 and 0.5. Both inputs are projected by independent linear layers to match the Transformer's hidden dimension.

The core of the authors' generative head is a stack of residual MLP blocks that progressively refine the initial noise into the final output vector. Each block follows a consistent architecture: it first fuses the current representation with the hidden state through two linear layers, creating a context-dependent transformation of the noise. This is followed by a SwiGLU activation layer—a modern, efficient nonlinearity. A residual connection then adds the block's input to its output, enabling stable gradient flow.

The authors set the number of MLP blocks to one quarter the number of Transformer layers, making the entire generative head account for only about 10 percent of total model parameters. This design choice keeps the computational overhead minimal while providing sufficient representational capacity.

For the input side, an intuitive approach would be to embed the predicted latent vectors from the previous step and feed them directly into the Transformer. However, the authors found this leads to noticeable performance degradation—the model struggles to unpack semantic information from such a compact representation.

Instead, the authors ground the autoregressive process in discrete token space. During training, they form the input for each step from the K tokens of the previous chunk. A lightweight two-layer MLP compresses these K token embeddings into a single input representation for the Transformer.

The inference process the authors implement unfolds as follows. At each step, the K tokens generated in the previous step are embedded and compressed into a single representation that serves as input to the Transformer. The Transformer processes this input and outputs a hidden state, which the generative head uses to predict the next continuous latent vector. This predicted latent vector is immediately passed through the frozen autoencoder decoder to reconstruct the K tokens for the next step, completing the feedback loop. This design maintains a clear connection to the discrete token space while operating on continuous representations internally.
