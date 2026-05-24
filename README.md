# SnapClass

SnapClass is an AI-powered attendance management system built with Streamlit. It uses face recognition for student login and classroom attendance, optional voice-based attendance, and Supabase for storing students, teachers, subjects, enrollments, and attendance records.

## Features

- Student login using face recognition
- New student profile registration with face embedding
- Optional voice enrollment for voice-based attendance
- Teacher login and registration with bcrypt password hashing
- Teacher dashboard for managing subjects
- Subject enrollment using subject codes / join links
- Face-based attendance from classroom photos
- Voice-based attendance for enrolled students
- Attendance records dashboard
- Supabase database integration
- Streamlit-based web interface

## Tech Stack

- Python
- Streamlit
- Supabase
- dlib
- scikit-learn
- NumPy
- Pandas
- Pillow
- bcrypt
- librosa
- resemblyzer
- segno

## Project Structure

```text
SNAPCLASS/
├── app.py
├── requirements.txt
├── src/
│   ├── screens/
│   │   ├── home_screen.py
│   │   ├── student_screen.py
│   │   └── teacher_screen.py
│   ├── database/
│   │   ├── config.py
│   │   └── db.py
│   ├── pipelines/
│   │   ├── face_pipeline.py
│   │   └── voice_pipeline.py
│   ├── components/
│   └── ui/
└── .streamlit/
    └── secrets.toml ```

```

## Database Tables
The app expects these Supabase tables:

- students
- teachers
- subjects
- subject_students
- attendance_logs
- Main stored data includes student face embeddings, optional voice embeddings, teacher credentials, subjects, enrollments, and attendance logs.

```
Setup
Install dependencies:

pip install -r requirements.txt
Create .streamlit/secrets.toml:

SUPABASE_URL = "your-supabase-project-url"
SUPABASE_KEY = "your-supabase-key"
Run the app:    

streamlit run app.py
```

## How It Works
Students log in by capturing a face image. The app extracts a face embedding and compares it with stored student embeddings. If the face is recognized, the student dashboard opens. If not recognized, the student can register a new profile.

Teachers log in with username and password. After login, teachers can create subjects, share join codes, take attendance using classroom photos, use voice attendance, and view attendance records.
--- 

## Deployment
This app can be deployed on Streamlit Community Cloud. Add the Supabase credentials in Streamlit secrets before running the hosted app.
---

### Important Notes
Face recognition accuracy depends on the quality and number of registered face images. For better results, each student should ideally have multiple face samples. A strict matching threshold should be used to reduce wrong logins.
---

### Author
Created by Aman.
