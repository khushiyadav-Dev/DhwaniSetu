def _photo_css():
    here = os.path.dirname(os.path.abspath(__file__))
    mimes = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}
    for ext in ("jpg", "jpeg", "png", "webp"):
        path = os.path.join(here, "assets", f"bridge.{ext}")
        if os.path.exists(path):
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            st.sidebar.success("Bridge photo loaded ✅")
            return ("background: linear-gradient(rgba(10,20,50,.35), rgba(10,20,50,.35)),"
                    f"url(data:image/{mimes[ext]};base64,{b64}) center/cover fixed;")
    st.sidebar.warning("assets/bridge.jpg nahi mila")
    return ("background: linear-gradient(-45deg,#1d3557,#457b9d,#e63946,#ffb703,#06d6a0);"
            "background-size: 400% 400%; animation: flow 18s ease infinite;")