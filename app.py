import glob, os, json, tempfile
import pandas as pd
import streamlit as st
from extractor import extract
from validator import validate

st.set_page_config(page_title="Receipt Extractor", layout="wide")
st.title("Receipt & Invoice Extractor")

COLORS = {"high": "#d4edda", "medium": "#fff3cd", "low": "#f8d7da", "missing": "#e2e3e5"}

versions = sorted(os.path.splitext(os.path.basename(p))[0] for p in glob.glob("prompts/*.txt"))

with st.sidebar:
    version = st.selectbox("Prompt version", versions, index=len(versions) - 1)
    mode = st.radio("Image source", ["Upload", "URL", "Sample"])
    source, preview = None, None
    if mode == "Upload":
        f = st.file_uploader("Upload image", type=["jpg", "jpeg", "png", "webp"])
        if f:
            suffix = os.path.splitext(f.name)[1]
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp.write(f.getvalue())
            tmp.close()
            source, preview = tmp.name, f.getvalue()
    elif mode == "URL":
        u = st.text_input("Image URL")
        if u:
            source, preview = u, u
    else:
        samples = sorted(glob.glob("samples/*.jpg") + glob.glob("samples/*.png"))
        s = st.selectbox("Sample image", samples)
        if s:
            source, preview = s, s
    user_prompt = st.text_area("Extra instruction (optional)", placeholder="e.g. Amounts are in INR")
    run = st.button("Extract", type="primary", disabled=source is None)

left, right = st.columns(2)
with left:
    if preview:
        st.image(preview, caption="Input image", use_container_width=True)

if run:
    with st.spinner("Extracting..."):
        try:
            r = extract(source, user_prompt, version)
            st.session_state["result"] = (r, validate(r))
        except Exception as e:
            st.session_state.pop("result", None)
            st.error(f"Extraction failed: {e}")

with right:
    if "result" in st.session_state:
        r, v = st.session_state["result"]
        if v["status"] == "ok":
            st.success("All checks passed.")
        elif v["status"] == "review":
            st.warning("Verify manually: one or more fields are uncertain or inconsistent.")
        else:
            st.error("This image is not a receipt or invoice.")
        st.caption(f"Document type: {r.document_type}")

        if v["status"] != "reject":
            rows = []
            conf = r.confidence.model_dump()
            for f in ["merchant", "date", "currency", "subtotal", "tax", "total"]:
                rows.append({"Field": f, "Value": getattr(r, f), "Confidence": conf[f], "Status": v["field_status"][f]})
            df = pd.DataFrame(rows)
            styled = df.style.apply(lambda row: [f"background-color: {COLORS[row['Status']]}; color: black"] * len(row), axis=1)
            st.dataframe(styled, use_container_width=True, hide_index=True)

            st.subheader(f"Items (confidence {conf['items']}, status {v['field_status']['items']})")
            st.dataframe(pd.DataFrame([i.model_dump() for i in r.items]), use_container_width=True, hide_index=True)

        if v["issues"]:
            st.subheader("Issues")
            for i in v["issues"]:
                st.write("- " + i)
        if r.notes:
            st.info(r.notes)

        out = {"extraction": r.model_dump(), "validation": v}
        st.download_button("Download JSON", json.dumps(out, indent=2, ensure_ascii=False), file_name="result.json", mime="application/json")
