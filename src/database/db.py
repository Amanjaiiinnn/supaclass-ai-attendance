from src.database.config import execute_supabase, supabase
import bcrypt  #hashing library for password security



def hash_pass(pwd):  #hashing the password using bcrypt, returns the hashed password as a string
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())

# compare hashed password with the provided password, no need to decode the hashed password as bcrypt.checkpw can handle byte strings

def check_teacher_exists(username):
    # Check for unique username, returns false when username is already taken and match when username is available
    response = execute_supabase(
        supabase.table("teachers").select("username").eq("username", username),
        "Check teacher username",
    ) #username match query to check if the username already exists in the database
    return len(response.data) > 0 



def create_teacher(username, password, name):

    data = { "username" : username, "password": hash_pass(password), "name": name}
    response = execute_supabase(
        supabase.table("teachers").insert(data),
        "Create teacher",
    )
    return response.data


def teacher_login(username, password):
    response = execute_supabase(
        supabase.table("teachers").select("*").eq("username", username),
        "Teacher login",
    )
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
            return teacher
    return None


def get_all_students():
    response = execute_supabase(
        supabase.table('students').select("*"),
        "Load students",
    )
    return response.data

def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {'name': new_name, 'face_embedding':face_embedding, "voice_embedding": voice_embedding}
    response = execute_supabase(
        supabase.table('students').insert(data),
        "Create student",
    )
    return response.data


def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    response = execute_supabase(
        supabase.table("subjects").insert(data),
        "Create subject",
    )
    return response.data

def get_teacher_subjects(teacher_id):
    response = execute_supabase(
        supabase.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id),
        "Load teacher subjects",
    )
    subjects = response.data


    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_logs', [])
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions


        sub.pop('subject_student', None)
        sub.pop('attendance_logs', None)

    return subjects


def  enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, "subject_id": subject_id}
    response= execute_supabase(
        supabase.table('subject_students').insert(data),
        "Enroll student",
    )
    return response.data


def  unenroll_student_to_subject(student_id, subject_id):
    response= execute_supabase(
        supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id),
        "Unenroll student",
    )
    return response.data



def get_student_subjects(student_id):
    response = execute_supabase(
        supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id),
        "Load student subjects",
    )
    return response.data


def get_student_attendance(student_id):
    response = execute_supabase(
        supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id),
        "Load student attendance",
    )
    return response.data


def create_attendance(logs):
    response = execute_supabase(
        supabase.table('attendance_logs').insert(logs),
        "Save attendance",
    )
    return response.data

def get_attendance_for_teacher(teacher_id):
    response = execute_supabase(
        supabase.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id),
        "Load teacher attendance",
    )
    return response.data
