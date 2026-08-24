import streamlit as st
import segno
import io


@st.dialog("Share code")
def share_subject_dialog(subject_name, subject_code):
    appdomain = "https://shaik-zabi-321-snap-class-app-mvgk3n.streamlit.app"
    joinurl = f"{appdomain}/?join_code={subject_code}"
    st.header("Scan to Join")

    qr = segno.make(joinurl)
    out = io.BytesIO()
    qr.save(out, kind='png', scale=10, border=1)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### copylink")
        st.code(joinurl, language='text')
        st.info("copy link to share ")
    with col2:
        st.markdown("### scan to join")
        st.image(out.getvalue(), use_container_width=True,
                 caption="Qr code for joining the class")
