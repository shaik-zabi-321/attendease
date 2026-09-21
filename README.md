# AttendEase

**Attendance, without the hassle.**

AttendEase is an AI-powered classroom attendance system that marks students present using **face recognition** from a single group photo, or **voice recognition** from a short classroom recording — no roll call, no manual entry.

---

## What it does

- **Teachers** take a photo of the whole class (or record a short audio clip), and the system automatically detects and matches enrolled students, marking attendance in seconds.
- **Students** log in with their face — first-time faces trigger a quick registration flow (name + optional voice sample).
- Teachers can create and manage subjects, share a join code/QR link for students to enroll, review and correct attendance before saving, and view attendance history per subject.
- Students can view their enrolled subjects and attendance stats.

---

## How recognition works

- **Face matching**: uses `dlib`'s face detection and 128-dimension face embeddings. A new face is compared directly against every registered student's stored embedding (nearest-neighbor matching), and only accepted as a match if the closest one is within a set distance threshold — an unregistered face correctly finds no match instead of being forced into an existing student's identity.
- **Voice matching**: uses `resemblyzer` voice embeddings. Classroom audio is split into speech segments (silence-based), and each segment is compared against enrolled students' voice profiles.
- Both approaches run **entirely on the server** — no third-party AI API calls, no student biometric data leaves the app's own infrastructure.

---

## Tech stack

| Layer | Technology |
|---|---|
| App framework | Streamlit |
| Database | Supabase (Postgres) |
| Face recognition | dlib, face_recognition_models |
| Voice recognition | Resemblyzer, librosa |
| Auth | bcrypt (password hashing) |
| QR / sharing | segno |

---

## Project structure

```
├── app.py                     # Entry point, routes between screens
├── requirements.txt
├── assets/                    # Logo and static images
├── .streamlit/
│   └── secrets.toml           # Supabase credentials (not committed)
├── src/
│   ├── screens/                # home_screen.py, teacher_screen.py, student_screen.py
│   ├── components/              # Dialogs: create subject, enroll, share, add photos, etc.
│   ├── pipelines/               # facepipeline.py, voice_pipeline.py
│   ├── database/                # config.py (Supabase client), db.py (queries)
│   └── ui/
│       └── style_base_layout.py # Colors, fonts, button styles
```

---

## Setup

1. **Clone the repo and create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add Supabase credentials**
   Create `.streamlit/secrets.toml`:
   ```toml
   SUPABASE_URL = "your-project-url"
   SUPABASE_PUBLISHABLE_KEY = "your-key"
   ```

4. **Set up the database**
   In Supabase, create tables: `teachers`, `students`, `subjects`, `subject_students`, `attendance_logs` (see `src/database/db.py` for the exact fields each query expects).

5. **Run it**
   ```bash
   streamlit run app.py
   ```

For faster local development, add `.streamlit/config.toml`:
```toml
[server]
runOnSave = true
```

---

## Known limitations

- **Single-photo enrollment**: each student currently enrolls with one reference photo, which limits face-matching accuracy compared to multiple photos per person. A confirmation step ("We think this is you — is that right?") is used at login to catch mismatches before granting access.
- **Free-tier hosting**: running on Streamlit Community Cloud's free tier caps available memory/CPU, which can cause noticeable lag under concurrent use — fine for a single classroom, not yet suited for scale.
- **Subject codes are freely typed**, which can lead to inconsistent naming across teachers.

---

## Roadmap

- [ ] Multiple enrollment photos per student for stronger face matching
- [ ] Move off Streamlit to a FastAPI backend + custom frontend (fixes camera/rear-lens control and reduces latency)
- [ ] Attendance defaulter tracking (flag students below attendance threshold)
- [ ] CSV/Excel export for department reporting
- [ ] HOD/Admin dashboard across all teachers
- [ ] Year + section based subject assignment for core subjects (removing manual enrollment where a whole section attends together), alongside the existing join-code flow for electives

---

## Credits

Built by **[shaik zabiulla]**, with guidance from **[apna college]**
