# Generative Head for Continuous Prediction

## Original Text

Generative modeling of continuous data is a well-established field, foundational to domains such as image and audio synthesis where data is inherently continuous. A promising recent paradigm combines these approaches with autoregressive models: a Transformer backbone predicts a conditioning hidden state, which is used by a subsequent generative model to produce the continuous output for each step.

Our Continuous Autoregressive Language Models (CALM) adapts this paradigm, but with a critical focus on computational efficiency that constrains the design of this generative component. We therefore conceptualize this component as a lightweight generative head.

Formally, the generative head is a stochastic function that takes the Transformer's hidden state, $h_{i-1} \in \mathbb{R}^d$, and draws a sample $z_i \in \mathbb{R}^l$ from the conditional distribution:

$$h_{i-1} = \text{Transformer}(z_{1:i-1}), \quad z_i \sim p(\cdot | h_{i-1})$$

While the generative head can be any continuous generative model, prominent options like Diffusion or Flow Matching are misaligned with our goal of efficiency. These models rely on an iterative sampling process—requiring dozens or even hundreds of network evaluations to produce a single vector—which directly counteracts the speedup gained from reducing the number of autoregressive steps.

## Teacher

Generative modeling of continuous data is well-established, foundational to domains like image and audio synthesis. A promising recent paradigm combines generative models with autoregressive models: a Transformer backbone predicts a conditioning hidden state, which is then used by a subsequent generative model to produce the continuous output for each step.

The authors adapt this paradigm to their continuous autoregressive language model, but with a critical constraint: computational efficiency. They conceptualize this component as a lightweight generative head—a term reflecting its role as a fast, single-forward-pass prediction mechanism rather than a full generative model.

Formally, the generative head is a stochastic function that takes the Transformer's hidden state and draws a sample from the conditional distribution given that state. In principle, this component could be implemented using any continuous generative model. Prominent options like Diffusion models or Flow Matching have proven powerful for image and audio generation. However, these approaches rely on an iterative sampling process—requiring dozens or even hundreds of network evaluations to produce a single vector. This directly counteracts the speedup the authors aim to achieve by reducing the number of autoregressive steps.

The authors' architecture therefore demands something different: a generative head capable of high-quality, single-step generation. This efficiency constraint shapes everything that follows. Instead of iterating toward the answer, the model must produce a high-quality sample immediately, given only the Transformer's hidden state. The authors address this challenge through an energy-based objective, departing from the iterative refinement paradigm dominant in recent generative modeling.
