# Discrete Token Input Strategy

## Original Text

An intuitive approach for the model's input would be to embed the predicted latent vectors $z_{i-1}$ from the previous step into the Transformer's hidden dimension $d$ using a linear projection. However, we empirically found that using these latent vectors as input for the Transformer leads to a noticeable degradation in performance, as the model struggles to unpack the semantic information from such a compact input representation.

To circumvent this, we ground the model's autoregressive process in the discrete token space. During training, the input for each step is formed by the $K$ tokens from the previous step. To maintain efficiency, we use a lightweight input compression module—a two-layer MLP—to map the $K$ embeddings into a single input representation.

The inference process unfolds as follows:

1. **Input Processing**: At step $i$, the previously generated chunk of $K$ tokens are embedded and compressed into a single input representation and fed into the Transformer.

2. **Continuous Prediction**: The Transformer outputs the hidden state $h_{i-1}$, which our energy-based generative head then uses to predict the next continuous vector, $z_i$.

3. **Discrete Feedback Loop**: The predicted vector $z_i$ is immediately passed through the frozen decoder of our pre-trained autoencoder, $g_{dec}$, to reconstruct the next $K$ discrete tokens.

## Teacher

An intuitive approach would be to use the predicted latent vectors directly as input to the Transformer—simply projecting each vector into the Transformer's hidden dimension. However, the authors empirically found this leads to noticeable performance degradation. The model struggles to unpack the semantic information from such a compact input representation.

To circumvent this, the authors ground their autoregressive process in discrete token space. During training, the input for each step consists of the K tokens from the previous chunk. To maintain efficiency—remember, the goal is to process K tokens in a single autoregressive step—they use a lightweight input compression module, a two-layer MLP, to map the K token embeddings into a single input representation.

This creates an interesting hybrid architecture. The model operates autoregressively in continuous latent space for prediction, but anchors itself in discrete token space for input processing. <break time="0.8s" /> The inference process unfolds in three stages.

First, input processing. <break time="0.3s" /> At step i, the previously generated chunk of K tokens are embedded and compressed into a single input representation, then fed into the Transformer.

Second, continuous prediction. <break time="0.3s" /> The Transformer outputs a hidden state, which the energy-based generative head uses to predict the next continuous vector.

Third, the discrete feedback loop. <break time="0.3s" /> The predicted vector passes immediately through the frozen decoder of the pre-trained autoencoder, reconstructing the next K discrete tokens. These tokens then become the input for the next step, completing the cycle.

This discrete grounding ensures the Transformer receives rich semantic input—while still achieving the efficiency gains from predicting multiple tokens at once through the continuous latent space.