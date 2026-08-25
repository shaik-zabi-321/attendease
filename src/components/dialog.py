import streamlit as st
from src.database.db import create_subjects


@st.dialog("Create new subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of subjects")

    sub_id = st.text_input("Enter subject ID", placeholder="eg 101")
    if sub_id and not sub_id.isdigit():
        st.error("please use only numbers")
        return
    sub_name = st.text_input("Enter Subject name",
                             placeholder="machine learning")
    sub_sec = st.text_input("Enter section ", placeholder="AI/CSE")
    if st.button("Create subject"):
        if sub_id and sub_name and sub_sec:
            try:
                create_subjects(sub_id, sub_name, sub_sec, teacher_id)
                st.toast("subject sucessfully created")
                st.rerun()
            except Exception as e:
                if getattr(e, "code", None) == "23505":
                    st.error(
                        "Subject ID already exists. Please choose a different ID.")
                else:
                    st.error(
                        "Something went wrong while creating the subject. Please try again.")
