from resemblyzer import VoiceEncoder, preprocess_wav #preprocess and normalize  to fit model input
import numpy as np 
import io  # load audio files
import librosa
import streamlit as st


@st.cache_resource 
def load_voice_encoder():
    return VoiceEncoder()


def get_voice_embedding(audio_bytes): # audio bytes from frontend, load encoder, preprocess audio, get embedding, return embedding as list to store in db.
    try:
        encoder = load_voice_encoder()


#more sr means better quality but more computationally expensive
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000) # librosa load audio from bytes, resample to 16kHz which is standard for voice recognition models, gives audio time series and sample rate.
        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav) #gives embedding about 256D.
        return embedding.tolist()
    except Exception as e:
        st.error('Voice recog error')
        return None
    

def identify_speaker(new_embedding, candidates_dict, threshold=0.65): #identify Speaker by audio embedding, compare with candidates dict of stored embeddings.
    if new_embedding is None or not candidates_dict:
        return None, 0.0  # if no new embedding or candidates, return None and score 0.0
    
    best_sid = None
    best_score = -1.0 # initialize best score to lowest possible value and replace it

    for sid, stored_embedding in candidates_dict.items(): #loop through candidates dict, get stored embedding for each candidate.
        if stored_embedding:
            similarity = np.dot(new_embedding, stored_embedding)#dat product.   
            if similarity> best_score:
                best_score = similarity
                best_sid = sid # replace best sid with current candidate if similarity is higher than best score.

    if best_score >= threshold:
        return best_sid, best_score
    
    return None, best_score



def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65): #break audio into segments, get embedding for each segment.

    try:
        encoder = load_voice_encoder()

        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)  
        segments = librosa.effects.split(audio, top_db=30) # split audio into segments based on silence(sensitivity controll of audio), top_db is the threshold for silence, lower means more sensitive to silence.

        identified_results = {}


        for start, end in segments:

            if (end-start) < sr * 0.5: #for garbage voice segments less than 0.5 seconds, skip them.
                continue
            segment_audio = audio[start:end] #processing audio segment, get the segment from start to end time.
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)


            sid, score = identify_speaker(embedding, candidates_dict, threshold) # passind everything.

            if sid:
                if sid not in identified_results or score > identified_results[sid]: # if sid is already identified but current score is better than previous score, update the score for that sid in identified results.
                    identified_results[sid] = score

        return identified_results
    except Exception as e:
        st.error('Bulk process error')
        return {}