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