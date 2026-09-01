import dlib
import numpy as np
import face_recognition_models
import streamlit as st
from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    return detector, sp, facerec


def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()
    faces = detector(image_np, 1)
    embeddings = []
    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(
            image_np, shape, 1)  # 128 embeddings
        embeddings.append(np.array(face_descriptor))
    return embeddings


@st.cache_resource
def get_trained_model():
    x = []
    y = []

    student_db = get_all_students()
    if not student_db:
        return None
    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            x.append(np.array(embedding))
            y.append(student.get('student_id'))
    if len(x) == 0:
        return 0
    return {'x': x, 'y': y}


def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)


def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)
    detected_students = {}
    model_data = get_trained_model()
    if not model_data:
        return detected_students, [], len(encodings)

    x_train = model_data['x']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))
    resemblance_threshold = 0.5

    for encoding in encodings:
        # compare against every registered student's embedding directly,
        # instead of trusting a forced single-class prediction
        distances = [np.linalg.norm(np.array(x) - encoding) for x in x_train]
        best_idx = int(np.argmin(distances))
        best_match_score = distances[best_idx]

        if best_match_score <= resemblance_threshold:
            predicted_id = int(y_train[best_idx])
            detected_students[predicted_id] = True

    return detected_students, all_students, len(encodings)
