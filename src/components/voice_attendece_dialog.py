import streamlit as st
from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
from datetime import datetime
import pandas as pd
from src.components.attendence_log import show_attendance_results


@st.dialog('Voice Attendence')
def voice_attendence_dialog(selected_subject_id):
    st.write(
        "Record audio of students saying iam present the AI will recognize the Studnts ")
    audio_data = None
    audio_data = st.audio_input("Record Class Room Audio")
    if st.button("Analyze Audio", width='stretch', type='primary'):
        with st.spinner("Processing Audio Data"):
            enrolled_res = supabase.table('subject_students').select(
                "*,students(*)").eq('subject_id', selected_subject_id).execute()
            enrolled_students = enrolled_res.data
            if not enrolled_students:
                st.warning("No students are enrolled in this subject yet.")
                return
            candidate_dict = {
                s['students']['student_id']: s['students']['voice_embedding']
                for s in enrolled_students if s['students'].get('voice_embedding')
            }
            if not candidate_dict:
                st.error('No enrolled students have voice profiles registered')
                return
            audio_bytes = audio_data.read()
            detected_scores = process_bulk_audio(audio_bytes, candidate_dict)
            results, attendence_to_logs = [], []
            results, attendence_to_log = [], []
            current_time_stamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            for node in enrolled_students:
                student = node['students']

                score = detected_scores.get(student['student_id'])
                is_present = score is not None

                results.append({
                    "Name": student['name'],
                    "Id": student['student_id'],
                    "Source": f"{score:.2f}" if is_present else "-",
                    "Status": "Present" if is_present else "Absent"
                })

                attendence_to_logs.append({
                    "student_id": student['student_id'],
                    "subject_id": selected_subject_id,
                    "timestamp": current_time_stamp,
                    "is_present": bool(is_present)
                })
            st.session_state.voice_attendence_results = (
                pd.DataFrame(results), attendence_to_logs)
    if st.session_state.get('voice_attendence_results'):
        st.divider()
        df_results, attendence_logs = st.session_state.voice_attendence_results
        show_attendance_results(df_results, attendence_logs)
