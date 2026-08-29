import streamlit as st

# Beep color palette
BEEP_GREEN = "#58B92E"
DEEP_FOREST = "#2F6B14"
WARM_ORANGE = "#FF9F43"
CREAM = "#FFF6EC"
SUNSHINE_AMBER = "#FFC800"
CORAL = "#FF6B57"
SLATE_GRAY = "#5F5E5A"


def style_background_home():
    st.markdown(f"""
        <style>
                .stApp {{
                    background: {WARM_ORANGE} !important;
                }}

                .stApp div[data-testid="stColumn"]{{
                    background-color: {CREAM} !important;
                    padding: 2.5rem !important;
                    border-radius: 3rem !important;
                    }}
        </style>
                """, unsafe_allow_html=True)


def style_background_dashboard():
    st.markdown(f"""
        <style>
                .stApp {{
                    background: {CREAM} !important;
                }}
        </style>
                """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

            #MainMenu, footer, header {{
                visibility: hidden;
            }}

            .block-container {{
                padding-top: 1.5rem !important;
            }}

            h1 {{
                font-family: 'Baloo 2', sans-serif !important;
                font-weight: 800 !important;
                font-size: 3rem !important;
                color: {DEEP_FOREST} !important;
                line-height: 1.1 !important;
                margin-bottom: 0rem !important;
            }}

            h2 {{
                font-family: 'Baloo 2', sans-serif !important;
                font-weight: 800 !important;
                font-size: 1.8rem !important;
                color: {DEEP_FOREST} !important;
                line-height: 0.9 !important;
                margin-bottom: 0rem !important;
            }}

            h3, h4, p {{
                font-family: 'Outfit', sans-serif;
                color: {SLATE_GRAY};
            }}

            /* primary = main action, e.g. "Snap the class" */
            button[kind="primary"] {{
                border-radius: 1.2rem !important;
                background-color: {BEEP_GREEN} !important;
                color: {CREAM} !important;
                border: none !important;
                border-bottom: 4px solid {DEEP_FOREST} !important;
                padding: 10px 20px !important;
                font-weight: 700 !important;
                transition: transform 0.15s ease-in-out !important;
                }}

            [data-testid="stCameraInputButton"] {{
                border-radius: 1.2rem !important;
                background-color: {BEEP_GREEN} !important;
                color: {CREAM} !important;
                border: none !important;
                border-bottom: 4px solid {DEEP_FOREST} !important;
                font-weight: 700 !important;
                padding: 10px 20px !important;
            }}

            [data-testid="stCameraInputButton"]:disabled {{
                opacity: 0.5 !important;
                cursor: not-allowed !important;
            }}

            /* secondary = alternate action, e.g. "Use voice instead" */
            button[kind="secondary"] {{
                border-radius: 1.2rem !important;
                background-color: {SUNSHINE_AMBER} !important;
                color: {DEEP_FOREST} !important;
                border: none !important;
                border-bottom: 4px solid #B38600 !important;
                padding: 10px 20px !important;
                font-weight: 700 !important;
                transition: transform 0.15s ease-in-out !important;
                }}

            /* tertiary = low emphasis, e.g. "Clear", "Logout" */
            button[kind="tertiary"] {{
                border-radius: 1.2rem !important;
                background-color: transparent !important;
                color: {DEEP_FOREST} !important;
                border: 2px solid {DEEP_FOREST} !important;
                padding: 8px 18px !important;
                font-weight: 700 !important;
                transition: transform 0.15s ease-in-out !important;
                }}

            button:hover {{
                transform: scale(1.04);
                }}
        </style>
                """, unsafe_allow_html=True)
