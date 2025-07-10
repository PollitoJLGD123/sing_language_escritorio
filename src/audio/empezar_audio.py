
import pyttsx3

def start_audio(palabra):
    engine = pyttsx3.init()
    engine.setProperty('rate', 125)  # es para poder darle la velocidad
    engine.say(palabra)
    engine.runAndWait()