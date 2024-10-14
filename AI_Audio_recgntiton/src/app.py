
from fastapi import FastAPI
import speech_recognition as sr
from pydub import AudioSegment
import time

def convert_to_wav(audio_file):
    audio = AudioSegment.from_file(audio_file)
    wav_file = audio_file.replace(audio_file.split('.')[-1], 'wav')
    audio.export(wav_file, format='wav')
    return wav_file

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    
    if not file_path.endswith('.wav'):
        file_path = convert_to_wav(file_path)

    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        
        try:
            #Google Web Speech API
            text = recognizer.recognize_google(audio_data, language='fa-IR')
            return text
        except sr.UnknownValueError:
            return "متن قابل شناسایی نیست."
        except sr.RequestError as e:
            return f"خطا در ارتباط با سرویس: {e}"

audio_file = 'wav/AgADDhIAAiTn6VM.wav'  

start_time = time.time()  
transcription = transcribe_audio(audio_file)
end_time = time.time()  
execution_time = end_time - start_time 
print(f"زمان اجرای کد: {execution_time} ثانیه")

app = FastAPI()
@app.get("/")
def read_user():
    return {"text": transcription}
