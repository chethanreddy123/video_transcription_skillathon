# coding=utf8
from gtts import gTTS
import gradio as gr
import os
import speech_recognition as sr
from googletrans import Translator, constants
from pprint import pprint
from moviepy.editor import *
import streamlit as st

st.title("Course Video Language converter and Transcriptor")


def video_to_translate(file_obj,initial_language,final_language):
# Insert Local Video File Path
    videoclip = VideoFileClip(file_obj)
    # Insert Local Audio File Path
    videoclip.audio.write_audiofile("test.wav",codec='pcm_s16le')
# initialize the recognizer
    r = sr.Recognizer()

    if initial_language == "English":
        lang_in='en-US'
    elif initial_language == "Italian":
        lang_in='it-IT'
    elif initial_language == "Spanish":
        lang_in='es-MX'
    elif initial_language == "Russian":
        lang_in='ru-RU'
    elif initial_language == "German":
        lang_in='de-DE'
    elif initial_language == "Japanese":
        lang_in='ja-JP'
    elif initial_language == "Telugu":
        lang_in='te-IN'
    elif initial_language == "Hindi":
        lang_in='hi-IN'

    # open the file
    with sr.AudioFile("test.wav") as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data, language = lang_in)
        st.text_area("The transcripted text of the video:", text)

    if final_language == "English":
        lang='en'
    elif final_language == "Italian":
        lang='it'
    elif final_language == "Spanish":
        lang='es'
    elif final_language == "Russian":
        lang='ru'
    elif final_language == "German":
        lang='de'
    elif final_language == "Japanese":
        lang='ja'
    elif final_language == "Telugu":
        lang='te'
    elif final_language == "Hindi":
        lang='hi'

    print(lang)
    # init the Google API translator
    translator = Translator()
    translation = translator.translate(text, dest=lang)
    #translation.text
    trans=translation.text
    myobj = gTTS(text=trans, lang=lang, slow=False) 
    myobj.save("audio.wav") 
    # loading audio file
    audioclip = AudioFileClip("audio.wav")
    
    # adding audio to the video clip
    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    new_video="video_translated_"+lang+".mp4"
    videoclip.write_videofile(new_video)
    #return 'audio.wav'
    return new_video



uploaded_file = st.file_uploader("Choose a course Video file" , type = ['mp4'])


if uploaded_file != None:
    st.subheader("The Orginal Course Video in English")
    st.video(uploaded_file)
    print(uploaded_file.getvalue())
    file = uploaded_file.read()
    video_result = open("sample.mp4", 'wb')
    video_result.write(file)
    video_result.write(file)
    video_result.close()

    Language = st.selectbox("Select the language", ["Hindi" , "Telugu","Italian" , "Spanish" , "Russian" , "German" , "Japanese"])

    file = video_to_translate("sample.mp4","English",Language)

    if file:
        st.video(file)