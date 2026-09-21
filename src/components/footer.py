import streamlit as st
from src.components.header import get_base64_image, LOGO_PATH


def _render_footer():
    logo_b64 = get_base64_image(LOGO_PATH)
    html = (
        "<div style=\"margin-top:3rem; padding-top:1.5rem; border-top:2px solid #FFE0B8; "
        "display:flex; flex-direction:column; align-items:center; gap:6px;\">"
        "<div style=\"display:flex; align-items:center; gap:8px;\">"
        f"<img src='data:image/png;base64,{logo_b64}' style='height:26px;' />"
        "<span style=\"font-family:'Baloo 2', sans-serif; font-weight:800; "
        "color:#2F6B14; font-size:16px;\">AttendEase</span>"
        "</div>"
        "<p style=\"font-family:'Outfit', sans-serif; color:#5F5E5A; font-size:12px; margin:0;\">"
        "Face + voice attendance, built for your classroom</p>"
        "<p style=\"font-family:'Outfit', sans-serif; color:#B4B2A9; font-size:11px; margin:4px 0 0;\">"
        "Made by shaik zabiulla &nbsp;&middot;&nbsp; Rayalaseema university college of Engineering</p>"
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def footer_home():
    _render_footer()


def footer_dashboard():
    _render_footer()
