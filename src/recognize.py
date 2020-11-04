import speech_recognition as sr

r = sr.Recognizer()

def recognize_audio(audio_path: str, engine: str) -> str:
    harvard = sr.AudioFile(audio_path)
    with harvard as source:
        audio = r.record(source)
    try:
        if engine == 'google':
            return r.recognize_google(audio)
        elif engine == 'sphinx':
            return r.recognize_sphinx(audio)
    except sr.UnknownValueError:
        return ''
