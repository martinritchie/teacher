```
Algorithm 1: Gradient Descent
Input: Learning rate lr
for epoch in range(max_epochs):
    for batch in data:
        grad = compute_gradient(batch)
        theta -= lr * grad
```