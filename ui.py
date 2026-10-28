import base64, os
import streamlit as st

BRIDGE_SVG = """
<div class="bridge-wrap">
<svg viewBox="0 0 1200 200" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M0 150 Q300 20 600 150 T1200 150" stroke="#ffd166" stroke-width="5" fill="none"/>
  <g stroke="#ffd166" stroke-width="2" opacity=".8">
    <line x1="150" y1="60" x2="150" y2="150"/><line x1="300" y1="45" x2="300" y2="150"/>
    <line x1="450" y1="80" x2="450" y2="150"/><line x1="750" y1="80" x2="750" y2="150"/>
    <line x1="900" y1="45" x2="900" y2="150"/><line x1="1050" y1="60" x2="1050" y2="150"/>
  </g>
  <rect x="0" y="150" width="1200" height="10" fill="#e63946"/>
  <rect x="0" y="160" width="1200" height="40" fill="#1d3557" opacity=".6"/>
  <rect class="car" x="0" y="140" width="26" height="10" rx="4" fill="#06d6a0"/>
  <rect class="car c2" x="0" y="140" width="26" height="10" rx="4" fill="#ff9f1c"/>
</svg></div>
"""


def _photo_css():
    path = "assets/bridge.jpg"
    if os.path.exists(path):
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return ("background: linear-gradient(rgba(10,20,50,.35), rgba(10,20,50,.35)),"
                f"url(data:image/jpeg;base64,{b64}) center/cover fixed;")
    return ("background: linear-gradient(-45deg,#1d3557,#457b9d,#e63946,#ffb703,#06d6a0);"
            "background-size: 400% 400%; animation: flow 18s ease infinite;")


def apply_style():
    css = f"""
    <style>
    .stApp {{ {_photo_css()} }}
    @keyframes flow {{ 0%{{background-position:0% 50%}} 50%{{background-position:100% 50%}} 100%{{background-position:0% 50%}} }}
    @keyframes rise {{ from{{opacity:0; transform:translateY(30px)}} to{{opacity:1; transform:none}} }}
    @keyframes shine {{ to{{background-position:200% center}} }}
    @keyframes pop {{ 0%{{transform:scale(.8); opacity:0}} 70%{{transform:scale(1.05)}} 100%{{transform:scale(1); opacity:1}} }}
    @keyframes drive {{ from{{transform:translateX(-60px)}} to{{transform:translateX(1260px)}} }}
    .block-container {{
        background: rgba(255,255,255,.88); backdrop-filter: blur(8px);
        border-radius: 24px; padding: 2rem 2.5rem !important; margin-top: 2rem;
        box-shadow: 0 12px 40px rgba(0,0,0,.25); animation: rise .8s ease;
    }}
    h1 {{
        background: linear-gradient(90deg,#e63946,#ff9f1c,#06d6a0,#457b9d,#e63946);
        background-size: 200% auto; -webkit-background-clip: text;
        -webkit-text-fill-color: transparent; animation: shine 4s linear infinite;
    }}
    div[style*="font-size:22px"] {{ animation: pop .6s ease; box-shadow: 0 6px 20px rgba(0,0,0,.3); }}
    .bridge-wrap {{ position: fixed; left: 0; right: 0; bottom: 0; height: 140px;
        opacity: .45; pointer-events: none; z-index: 0; }}
    .bridge-wrap svg {{ width: 100%; height: 100%; }}
    .car {{ animation: drive 9s linear infinite; }}
    .car.c2 {{ animation-duration: 6s; animation-delay: 2s; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(BRIDGE_SVG, unsafe_allow_html=True)