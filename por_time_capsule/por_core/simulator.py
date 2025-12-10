import numpy as np

def run_chain(text: str, steps: int = 48, seed: int = 3):
    """Generate resonant chain of values for this text."""
    np.random.seed(seed)

    base = np.tanh(len(text) / 100.0)  # semantic baseline
    chain = [base]

    for i in range(1, steps):
        noise = np.random.normal(0, 0.05)
        drift = (chain[-1] - base) * -0.15
        new = chain[-1] + drift + noise
        chain.append(float(new))

    return np.array(chain)

