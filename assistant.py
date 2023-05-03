import os
import re
import time
import pyaudio
import speech_recognition as sr
import winsound
import openai

api_key = "API-KEY HERE"
os.system('title AI Voice Recognition using chatGPT')
lang = 'en'

openai.api_key = api_key

guy = ""
stop_flag = False

question_styles = ["so i'm", "so i am", "how many", "what are", "i'm trying", "i am trying", "hey", "what is", "what's the", "who was", "how does", "when do", "why is", "who is", "what are", "how can", "what should", "how do I", "what's the difference", "what happens if", "how do I troubleshoot", "what's the syntax", "how do I install", "what are the best practices", "what are the limitations of", "what's the typical use case", "what's the performance of", "what's the scalability of", "what's the security of", "how do I implement", "what are the parameters for", "how do I use", "what are the options for", "what is the output of", "what is the input of", "what are the different types of", "what is the relationship between", "what are the advantages of", "what is the role of", "how does it relate to", "what is the difference between", "what is the impact of", "what is the meaning of the term", "what is the algorithm for"]

def sanitize_text(text):
    clean_text = re.sub(r'[^a-zA-Z0-9\s.,]', '', text)
    return clean_text

while not stop_flag:
    def get_audio():
        global stop_flag
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"AI Voice chat bot Using ChatGPT")
        r = sr.Recognizer()
        r.energy_threshold = 4000
    
        with sr.Microphone(device_index=1) as source:
            audio = r.listen(source)
            said = ""
    
            try:
                said = r.recognize_google(audio)
                said = "Respond with a mafia boss accent " + said
                print(said)
                global guy
                guy = said
    
                if "stop" in said.lower() or "shut up" in said.lower():
                    winsound.PlaySound(None, winsound.SND_PURGE) # stop current sound
                    return
    
                question_detected = any(style in said.lower() for style in question_styles)
    
                if question_detected:
                    try:
                        winsound.PlaySound("fetching.wav", winsound.SND_ASYNC)
                        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": said}])
                    except openai.OpenAIError as e:
                        print("OpenAI error: {0}".format(e))
                        return
    
                    text = completion.choices[0].message.content
                    clean_text = sanitize_text(text)
                    print(f"{clean_text}")
    
                    # Use os.system to generate TTS audio and save it as an MP3 file
                    os.system(f'tts --text "{clean_text}" --model_name tts_models/en/ljspeech/vits--neon > {"nul" if os.name == "nt" else "/dev/null"} 2>&1')
    
                    # Play the saved MP3 file using winsound
                    winsound.PlaySound("tts_output.wav", winsound.SND_ASYNC)
    
                if "tell me again" in said.lower() or "please repeat" in said.lower():
                    winsound.PlaySound("tts_output.wav", winsound.SND_ASYNC)
    
            except sr.UnknownValueError:
                print("Speech Recognition could not understand audio")
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"AI Voice chat bot Using ChatGPT")
            except sr.RequestError as e:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"AI Voice chat bot Using ChatGPT")
                print("Could not request results from Speech Recognition service: {0}".format(e))
        return said

    get_audio()
