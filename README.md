## Demo

Hugging Face Space:  
`https://supaclass.streamlit.app/`

[Try the App](https://supaclass.streamlit.app/)

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
## Project Explanation

SnapClass is an AI-based attendance management system built using Streamlit and Supabase. The main goal of this project is to make student attendance faster, smarter, and easier by using face recognition and optional voice recognition.

The application has two main portals: Student and Teacher. Students can log in using FaceID. When a student captures their photo, the system detects the face, generates a face embedding, and compares it with the stored embeddings in the database. If the face is recognized, the student is logged in and can view enrolled subjects and attendance records. If the face is not recognized, the student can register a new profile.

Teachers can register and log in using a username and password. Passwords are securely hashed using bcrypt before being stored. After login, teachers can create subjects, share subject codes or join links, manage enrolled students, take attendance using classroom photos, and view attendance records.

For face recognition, the project uses dlib-based face embeddings and a machine learning classifier. Each detected face is converted into a numerical embedding, and the system predicts which student the face belongs to. A distance threshold is used to verify whether the detected face is close enough to a registered student.

The project also includes optional voice enrollment and voice attendance. If a student records their voice during registration, the system can later compare classroom audio with stored voice embeddings to help mark attendance.

Supabase is used as the backend database. It stores student profiles, teacher accounts, subjects, student-subject enrollments, face embeddings, voice embeddings, and attendance logs. Streamlit is used to build the user interface and manage the student and teacher dashboards.

Overall, SnapClass demonstrates how AI, computer vision, voice processing, and cloud databases can be combined to build a practical attendance system.  


### How It Works
Students log in by capturing a face image. The app extracts a face embedding and compares it with stored student embeddings. If the face is recognized, the student dashboard opens. If not recognized, the student can register a new profile.

Teachers log in with username and password. After login, teachers can create subjects, share join codes, take attendance using classroom photos, use voice attendance, and view attendance records.

### Deployment
This app can be deployed on Streamlit Community Cloud. Add the Supabase credentials in Streamlit secrets before running the hosted app.


### Important Notes
Face recognition accuracy depends on the quality and number of registered face images. For better results, each student should ideally have multiple face samples. A strict matching threshold should be used to reduce wrong logins.

### Author
Created by Aman.
