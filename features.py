import numpy as np
from scipy.io import wavfile
from scipy.fft import dct

SR = 22050
CLIP_LEN = 0.6
LABELS = ["Normal", "Warning", "Danger"]


def load_wav(path_or_file):
    sr, y = wavfile.read(path_or_file)
    if y.ndim > 1:
        y = y.mean(axis=1)
    if y.dtype.kind == "i":
        y = y / np.iinfo(y.dtype).max
    y = y.astype(np.float32)
    if sr != SR:
        n = int(len(y) * SR / sr)
        y = np.interp(np.linspace(0, len(y) - 1, n), np.arange(len(y)), y)
    return y.astype(np.float32)


def isolate_tap(y):
    y = y - np.mean(y)
    y = y / (np.max(np.abs(y)) + 1e-9)
    start = max(int(np.argmax(np.abs(y))) - int(0.005 * SR), 0)
    clip = y[start:start + int(CLIP_LEN * SR)]
    if len(clip) < int(CLIP_LEN * SR):
        clip = np.pad(clip, (0, int(CLIP_LEN * SR) - len(clip)))
    return clip


def _mel_filterbank(n_fft, n_mels=26, fmin=50, fmax=SR / 2):
    mel = lambda f: 2595 * np.log10(1 + f / 700)
    inv = lambda m: 700 * (10 ** (m / 2595) - 1)
    pts = inv(np.linspace(mel(fmin), mel(fmax), n_mels + 2))
    bins = np.floor((n_fft + 1) * pts / SR).astype(int)
    fb = np.zeros((n_mels, n_fft // 2 + 1))
    for i in range(1, n_mels + 1):
        l, c, r = bins[i - 1], bins[i], bins[i + 1]
        for k in range(l, c):
            fb[i - 1, k] = (k - l) / max(c - l, 1)
        for k in range(c, r):
            fb[i - 1, k] = (r - k) / max(r - c, 1)
    return fb


def spectrum(clip):
    n = len(clip)
    mag = np.abs(np.fft.rfft(clip * np.hanning(n)))
    freqs = np.fft.rfftfreq(n, 1 / SR)
    return freqs, mag


def extract_features(y):
    clip = isolate_tap(y)
    freqs, mag = spectrum(clip)
    power = mag ** 2
    tot = power.sum() + 1e-12

    centroid = (freqs * power).sum() / tot
    bandwidth = np.sqrt((((freqs - centroid) ** 2) * power).sum() / tot)
    cum = np.cumsum(power) / tot
    rolloff = freqs[np.searchsorted(cum, 0.85)]
    peak_freq = freqs[np.argmax(mag)]

    def band(lo, hi):
        return power[(freqs >= lo) & (freqs < hi)].sum() / tot
    low, mid, high = band(0, 1000), band(1000, 4000), band(4000, SR / 2)

    rms = np.sqrt(np.mean(clip ** 2))
    env = np.abs(clip)
    win = int(0.01 * SR)
    env = np.convolve(env, np.ones(win) / win, mode="same")
    above = np.where(env > 0.1 * env.max())[0]
    ring_time = (above[-1] - above[0]) / SR if len(above) else 0.0

    frame, hop = 1024, 512
    n_frames = 1 + (len(clip) - frame) // hop
    fb = _mel_filterbank(frame)
    frames = np.stack([clip[i * hop:i * hop + frame] * np.hanning(frame)
                       for i in range(n_frames)])
    p = np.abs(np.fft.rfft(frames, axis=1)) ** 2
    mel_e = np.log(p @ fb.T + 1e-10)
    mfcc = dct(mel_e, type=2, axis=1, norm="ortho")[:, :13].mean(axis=0)

    names = (["centroid", "bandwidth", "rolloff", "peak_freq",
              "low_energy", "mid_energy", "high_energy", "rms", "ring_time"]
             + [f"mfcc{i}" for i in range(13)])
    vec = np.array([centroid, bandwidth, rolloff, peak_freq, low, mid, high,
                    rms, ring_time, *mfcc], dtype=np.float32)
    return vec, names