import numpy as np, os
from scipy.io import wavfile
from features import SR

rng = np.random.default_rng(42)


def tap(freqs, decays, amps, noise=0.02, dur=0.8):
    t = np.arange(int(dur * SR)) / SR
    y = sum(a * np.sin(2 * np.pi * f * t + rng.uniform(0, 6.28)) * np.exp(-d * t)
            for f, d, a in zip(freqs, decays, amps))
    y += noise * rng.standard_normal(len(t)) * np.exp(-8 * t)
    y += 0.01 * rng.standard_normal(len(t))
    lead = np.zeros(int(rng.uniform(0.05, 0.2) * SR))
    return (np.concatenate([lead, y]) * 0.8).astype(np.float32)


def make(cls):
    j = lambda x, s=0.15: x * rng.uniform(1 - s, 1 + s)
    if cls == "Normal":
        return tap([j(3200), j(5200), j(7500)], [j(60), j(80), j(100)], [1, .6, .3])
    if cls == "Warning":
        return tap([j(1100), j(2300), j(3400)], [j(18), j(30), j(45)], [1, .7, .35])
    y = tap([j(450), j(900), j(1700)], [j(10), j(25), j(70)], [1, .8, .5], noise=0.08)
    y += 0.1 * rng.standard_normal(len(y)) * np.exp(-np.arange(len(y)) / SR * 6)
    return y.astype(np.float32)


if __name__ == "__main__":
    for cls in ["Normal", "Warning", "Danger"]:
        os.makedirs(f"data/demo/{cls}", exist_ok=True)
        for i in range(60):
            wavfile.write(f"data/demo/{cls}/{i:03d}.wav", SR, make(cls))
    print("Demo data ready: 180 clips in data/demo/")