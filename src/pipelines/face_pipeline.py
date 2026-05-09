import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC # classifier for face recognition
import streamlit as st

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():  #heavy lifting function to load the dlib models, cached to avoid reloading on every function call. saves memory
    detector = dlib.get_frontal_face_detector()  #bounding box detector


    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location() # landmark detector  by pose_predictor_model_location for face keypoints like eyes, nose, mouth
    )
#face recognition model that generates 128D embeddings for each detected face, become efficient like put heart into it  
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location() 
    )

    return detector, sp, facerec

def get_face_embeddings(image_np):  # create vector array
    detector, sp, facerec = load_dlib_models()
    faces = detector(image_np, 1) #can be 2 , 3 but utilize more cpu and give better result. like do reprocessing

    encodings= [] # image embeddings array to store.

    for face in faces: #shape predict 
        shape = sp(image_np, face) # gives the 68 facial landmarks for the detected face.
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1) #128 embedding

        encodings.append(np.array(face_descriptor)) # numpy  make easy calc of math op.
    return encodings # this gives no on faces.

@st.cache_resource #HEAVY function thus put in cache.
def get_trained_model(): #svc model train.
    X = []  # eg. embeddings
    y = []   # eg.  ids


    student_db = get_all_students()

    if not student_db:
        return None
    
    for student in student_db:
        embedding = student.get('face_embedding')  # if embedding exists for the student, get those embeding and put in model.
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))

    if len(X) ==0: # if not get embedding
        return 0
    
    #classifier , divde using linear kernel.
    clf = SVC(kernel='linear', probability=True, class_weight='balanced') # balance photos to 1 like 15 photos of one student and 1 photo of another student, it will balance the weights to avoid bias towards the student with more photos.

    try:
        clf.fit(X, y)
    except ValueError:
        pass

    return {'clf': clf, 'X':X, "y":y} # return the data we get.

#cache validation as whenever new student register or new face embedding added, we need to clear the cache to retrain the model with new data.
def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np): #TAKES CLASS IMAGE, DETECT FACES, GET EMBEDDINGS, PREDICT USING MODEL, RETURN DETECTED STUDENT IDS. 
    encodings = get_face_embeddings(class_image_np)

    detected_student = {}#INITIAL EMPTY


    model_data = get_trained_model()

    if not model_data:
        return detected_student, [], len(encodings)
    
    #GET Model classifier
    clf = model_data['clf']
    X_train = model_data['X']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train))) 

    for encoding in encodings: # get embeddings
        if len(all_students)>= 2:
            predicted_id= int(clf.predict([encoding])[0]) #if more than 2 students in the db, use the model to predict the student id by most scored encoding.
        else:
            predicted_id = int(all_students[0])

        student_embedding = X_train[y_train.index(predicted_id)] #index sane for X and y as they are trained together, get the embedding of the predicted student from the training data to compare with the current encoding.

        best_match_score = np.linalg.norm(student_embedding - encoding) #use linear algebra to calculate the distance between the predicted student's embedding and the current encoding, gives a score of how closely they match. lower score means better match.

        resemblance_threshold = 0.6
# like threeway check is done

        if best_match_score <= resemblance_threshold:
            detected_student[predicted_id] = True
    return detected_student, all_students, len(encodings) # return all students

