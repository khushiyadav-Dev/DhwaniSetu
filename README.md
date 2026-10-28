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