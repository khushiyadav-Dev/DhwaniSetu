import os, io, joblib, numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from features import load_wav, extract_features, isolate_tap, spectrum, SR
from ui import apply_style

st.set_page_config(page_title="DhwaniSetu", page_icon="🌉", layout="centered")
apply_style()

MSG = {
 "English": {
  "title": "🌉 DhwaniSetu", "sub": "Acoustic AI for Structural Safety",
  "how": "Tap the surface with a small hammer/rod, then record or upload the sound.",
  "rec": "🎙 Record the tap", "up": "…or upload a .wav file",
  "res": ["NORMAL – solid sound", "WARNING – hollow sound, get it checked",
          "DANGER – dull / cracked sound, call an engineer"],
  "conf": "Confidence", "disc": "Decision-support tool, not a certified structural-safety verdict.",
  "nomodel": "Model not found. Run: python generate_demo_data.py && python train.py"},
 "हिन्दी": {
  "title": "🌉 ध्वनिसेतु", "sub": "संरचनात्मक सुरक्षा के लिए ध्वनि-आधारित AI",
  "how": "सतह पर छोटे हथौड़े/रॉड से ठोकें, फिर आवाज़ रिकॉर्ड या अपलोड करें।",
  "rec": "🎙 ठोकने की आवाज़ रिकॉर्ड करें", "up": "…या .wav फ़ाइल अपलोड करें",
  "res": ["सामान्य – ठोस आवाज़", "चेतावनी – खोखली आवाज़, जाँच करवाएँ",
          "ख़तरा – दबी/दरार जैसी आवाज़, तुरंत इंजीनियर को बुलाएँ"],
  "conf": "भरोसा", "disc": "यह सहायक उपकरण है, प्रमाणित सुरक्षा रिपोर्ट नहीं।",
  "nomodel": "मॉडल नहीं मिला। चलाएँ: python generate_demo_data.py && python train.py"},
}
COLORS = ["#2e9e4f", "#f0a500", "#d62828"]

lang = st.sidebar.radio("Language / भाषा", list(MSG))
t = MSG[lang]
st.title(t["title"])
st.caption(t["sub"])
st.write(t["how"])

path = "models/dhwanisetu_rf.joblib"
if not os.path.exists(path):
    st.error(t["nomodel"])
    st.stop()
bundle = joblib.load(path)
model = bundle["model"]
if "demo" in bundle["source"]:
    st.sidebar.warning("Model trained on SYNTHETIC demo data. Add real taps for real accuracy.")
else:
    st.sidebar.info(f"Real-data test accuracy: {bundle['test_acc']:.0%}")

audio = st.audio_input(t["rec"]) if hasattr(st, "audio_input") else None
upload = st.file_uploader(t["up"], type=["wav"])
src = audio or upload

if src:
    y = load_wav(io.BytesIO(src.getvalue()))
    feats, _ = extract_features(y)
    proba = model.predict_proba([feats])[0]
    k = int(np.argmax(proba))
    st.markdown(
        f"<div style='background:{COLORS[k]};padding:18px;border-radius:12px;"
        f"color:white;font-size:22px;font-weight:700'>{t['res'][k]}</div>",
        unsafe_allow_html=True)
    st.progress(float(proba[k]), text=f"{t['conf']}: {proba[k]:.0%}")

    clip = isolate_tap(y)
    freqs, mag = spectrum(clip)
    c1, c2 = st.columns(2)
    fig, ax = plt.subplots(figsize=(4, 2.6))
    ax.plot(np.arange(len(clip)) / SR, clip)
    ax.set_title("Tap waveform")
    ax.set_xlabel("sec")
    c1.pyplot(fig)
    fig, ax = plt.subplots(figsize=(4, 2.6))
    ax.plot(freqs, mag)
    ax.set_xlim(0, 10000)
    ax.set_title("Frequency spectrum")
    ax.set_xlabel("Hz")
    c2.pyplot(fig)
st.info(t["disc"])