import streamlit as st
import base64
from pathlib import Path


@st.cache_data
def get_base64_image(path):
    img_bytes = Path(path).read_bytes()
    return base64.b64encode(img_bytes).decode()


LOGO_PATH = "C:\Users\shaik zabiulla\Desktop\SNAP_CLASS\assets\attendease_icon.png"


def header_home():
    logo_b64 = get_base64_image(LOGO_PATH)

    st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:20px; margin-top:20px">
            <img src='data:image/png;base64,{logo_b64}' style='height:110px;' />
            <h1 style='text-align:center; color:#2F6B14; margin-top:8px;'>AttendEase</h1>
            <p style='text-align:center; color:#5F5E5A; margin-top:-6px;'>Smile, say hi, you're marked present</p>
        </div>
                """, unsafe_allow_html=True)


def header_dashboard():
    logo_b64 = get_base64_image(LOGO_PATH)

    st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:center; gap:12px;">
            <img src='data:image/png;base64,{logo_b64}' style='height:70px;' />
            <h2 style='text-align:left; color:#2F6B14;'>AttendEase</h2>
        </div>
                """, unsafe_allow_html=True)
