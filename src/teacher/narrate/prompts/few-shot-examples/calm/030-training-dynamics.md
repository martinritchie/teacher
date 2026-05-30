# Training Dynamics and Learning Curves

To further investigate the learning dynamics of our framework, we plot the training curves of CALM-XL against the Transformer baselines. The baseline Transformer models exhibit rapid initial gains before their performance gradually begins to saturate.

In contrast, CALM-XL displays a more patient but ultimately steeper learning curve, initially trailing Transformer-M but progressively closing the performance gap with the Transformer-L model. We attribute this phenomenon to the different nature of the predictive task.

While the baseline models learn the relatively simple task of predicting a single, low-information discrete token, our CALM model must learn to model the complex, high-dimensional distribution of continuous vectors, which explains the slower initial progress. However, once this ability is established, the model can unlock the potential of its large parameter count, entering a phase of more significant and sustained improvements.

This learning pattern suggests that CALM models may benefit from longer training schedules or different learning rate schedules compared to discrete token baselines, as they require more time to build the capacity to model continuous distributions effectively.
