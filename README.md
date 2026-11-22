<div align="center">

# 🌉 DhwaniSetu

### Tap a concrete surface. Listen to the sound. Know if it is solid, hollow, or cracked.

**An acoustic AI screening tool for bridges and buildings — free, phone-friendly, English + Hindi.**

[![Live Demo](https://img.shields.io/badge/▶%20TRY%20THE%20LIVE%20APP-00D2FF?style=for-the-badge&logo=streamlit&logoColor=black)](https://dhwanis-mepxnw5imdendcfvmuogyb.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![Made in India](https://img.shields.io/badge/Made%20in-India%20🇮🇳-ff9933?style=for-the-badge)](https://github.com/khushiyadav-Dev)

<img src="assets/app-preview.png" alt="DhwaniSetu app screenshots" width="100%" />

</div>

---

## 🚨 The problem

Cracks and hollow pockets inside a bridge pier or a concrete wall are **invisible from the outside**. Professional sensor-based monitoring costs lakhs, so small municipalities, panchayats and private builders simply skip it.

Engineers already do the cheap version — **hammer-tap testing** — but it depends on a trained ear. A junior engineer, a contractor or a site supervisor cannot reliably tell a solid sound from a hollow one.

**DhwaniSetu turns that ear into software.** Tap the surface, record 2 seconds on any phone, and get a screening verdict with a confidence score.

> ⚠️ **It is a screening aid, not a certified safety report.** Final decisions must come from a qualified structural engineer.

---

## ⚙️ How it works

<img src="assets/pipeline.png" alt="DhwaniSetu pipeline" width="100%" />

1. **Record** a tap on the surface (mic on a phone is enough) or upload a `.wav` file.
2. **Isolate** the tap — the loudest transient is cut out as a fixed 0.6 s clip, so background noise before and after is ignored.
3. **Extract 22 features** — spectral centroid, bandwidth, rolloff, peak frequency, low/mid/high energy bands, RMS, ring-time, and 13 MFCCs (mel-frequency cepstral coefficients).
4. **Classify** with a Random Forest (300 trees, trained with 5-fold cross-validation).
5. **Return** `Normal` / `Warning` / `Danger` plus a confidence bar and the waveform + spectrum of that exact tap.

---

## 🔊 What the app actually hears

<img src="assets/signals.png" alt="Waveforms and spectra for the three classes" width="100%" />

| Verdict | Sound character | What it suggests |
|:--|:--|:--|
| 🟢 **Normal** | Short, bright, high-pitched ring (~3.4 kHz peak) | Solid, tight concrete |
| 🟠 **Warning** | Lower and longer ring (~1 kHz peak) | Possibly hollow — get it checked |
| 🔴 **Danger** | Dull, damped, noisy, very low (~440 Hz peak) | Possibly cracked — call an engineer |

The physics is simple and that is why it works: a solid mass reflects high frequencies back quickly, while a hollow or cracked volume lets energy escape and rings low and long.

---

## 📊 Model card

<img src="assets/model.png" alt="Confusion matrix and feature importance" width="100%" />

| | |
|:--|:--|
| **Model** | Random Forest, 300 trees |
| **Features** | 22 (9 spectral/temporal + 13 MFCCs) |
| **Training data** | 180 synthetic tap clips (60 per class) |
| **Validation** | 5-fold cross-validation + 25% held-out test |
| **Result** | 100% CV, 100% held-out |
| **Most important features** | `mfcc1`, `peak_freq`, `rolloff`, `mfcc2`, `centroid` |

**Read that 100% carefully — it is not a real-world result.** The clips are computer-generated from three different frequency/decay profiles, so the classes are cleanly separable by construction. Real taps have echoes, ambient traffic, hand noise and surface variation. A perfect score here means the pipeline is correct, not that the model is ready.

---

## ✨ Features

| | |
|:--|:--|
| 🎙 **Record or upload** | Works from a phone browser, no app install |
| 🌐 **English + Hindi** | Full UI translated, not just the title |
| 📊 **Explainable output** | Waveform + frequency spectrum for every verdict |
| 📱 **Installable** | "Add to home screen" turns it into a PWA-like tool |
| ⚖️ **Honest by design** | Synthetic-data warning is shown inside the app, not hidden |
| 🪶 **Lightweight** | Pure NumPy/SciPy feature extraction, no deep-learning runtime |

---

## 🖥️ Run it locally

```bash
git clone https://github.com/khushiyadav-Dev/DhwaniSetu.git
cd DhwaniSetu
pip install -r requirements.txt

python generate_demo_data.py     # 180 synthetic tap clips
python train.py                  # trains + saves models/dhwanisetu_rf.joblib
streamlit run app.py
```

To use **real recordings** instead of the synthetic set, drop your clips into
`data/real/Normal/`, `data/real/Warning/`, `data/real/Danger/` and run `train.py` again —
it picks `data/real` automatically when that folder exists.

---

## 🗂️ Project structure

```
DhwaniSetu/
├── app.py                  # Streamlit UI: recorder, uploader, verdict, plots
├── ui.py                   # Theme, gradient background, bridge animation
├── features.py             # Tap isolation · FFT · MFCC · ring-time → 22 features
├── generate_demo_data.py   # Synthetic tap generator (3 acoustic profiles)
├── train.py                # Random Forest + CV + held-out test
├── models/
│   └── dhwanisetu_rf.joblib
└── assets/                 # Screenshots and diagrams used in this README
```

---

## ⚠️ Limitations — please read before trusting it

- **Trained on synthetic sounds.** The 100% accuracy in the demo is not a field result.
- **Concrete surfaces only.** It cannot detect internal micro-cracks, cable corrosion or rebar damage.
- **Noise and tapping style change the answer.** A different hammer, angle or distance shifts the spectrum.
- **One tap is one opinion.** A real inspection averages many taps per location.
- **Decision support, not a verdict.** A qualified engineer must make the final call.

---

## 🗺️ Roadmap

- [ ] Collect 100+ real taps per class and publish **real** accuracy
- [ ] Test-history table with CSV export
- [ ] Offline mode (run the model fully in the browser)
- [ ] Vibration-based monitoring for continuous sensing
- [ ] More Indian languages (Marathi, Tamil, Bengali)

---

## 👩‍💻 Author

**Khushi Yadav** — B.Tech CSE (AI & ML), Lucknow
Cloud + AI/ML · building tools that turn messy signals into clear decisions.

[![GitHub](https://img.shields.io/badge/GitHub-khushiyadav--Dev-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/khushiyadav-Dev)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Khushi%20Yadav-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/khushi-yadav-6417213a7)
[![Email](https://img.shields.io/badge/Email-khushiyadav1254@gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:khushiyadav1254@gmail.com)

<sub>Built as a student project to explore audio feature engineering, classical ML, and end-to-end deployment. Feedback and real tap recordings are very welcome.</sub>






















# 🌉 DhwaniSetu — Acoustic AI for Structural Safety

A free, phone-friendly tool that listens to the **sound of a tap** on a concrete surface and flags it as **Normal / Warning / Danger**.

🔗 **Live demo:** https://dhwanis-mepxnw5imdendcfvmuogyb.streamlit.app

![DhwaniSetu screenshot](assets/screenshot.png)

## Why this project?
- Cracks and hollow spots inside bridges and buildings are **not visible to the eye**.
- Sensor-based monitoring is expensive, so small municipalities often cannot afford it.
- Engineers already use hammer-tap testing, but it depends on a **trained ear**. DhwaniSetu tries to make that first screening step simple and free.

## How it works
1. Tap the surface and record the sound (or upload a `.wav` file).
2. The app isolates the tap and extracts features: FFT spectrum, MFCC, ring-time and energy bands.
3. A **Random Forest** classifier gives a verdict with a confidence score.

| Sound | Meaning | Verdict |
|---|---|---|
| Short, bright, tight | Solid | 🟢 Normal |
| Lower, longer ring | Possibly hollow | 🟠 Warning |
| Dull, very low, damped | Possibly cracked | 🔴 Danger |

## Features
- 🎙 Record or upload a tap sound
- 🌐 English + Hindi interface
- 📊 Waveform and frequency-spectrum graphs
- 📱 Works in a phone browser (can be added to the home screen)

## Run locally
```bash
pip install -r requirements.txt
python generate_demo_data.py
python train.py
python -m streamlit run app.py
```

## Project files
- `features.py` — tap isolation, FFT, MFCC, ring-time
- `generate_demo_data.py` — synthetic tap sounds for the demo
- `train.py` — Random Forest training with cross-validation and a held-out test
- `app.py` / `ui.py` — Streamlit dashboard and styling

## ⚠️ Limitations (please read)
- The current model is trained on **synthetic (computer-generated) sounds**, so the ~100% accuracy seen in the demo is **not a real-world result**.
- It is meant for **concrete surfaces** and cannot detect internal micro-cracks or cable damage.
- Background noise and tapping style can change the result.
- This is a **decision-support tool, not a certified structural-safety verdict.** A qualified engineer must make the final call.

## Roadmap
- [ ] Record 100+ real taps per class and report real accuracy
- [ ] Test history table and CSV download
- [ ] More languages and offline mode
- [ ] Vibration-based monitoring mode

## Author
Made by **KHUSHI YADAV** — student project.
