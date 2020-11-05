import speech_recognition as sr

r = sr.Recognizer()

def recognize_audio(audio_path: str, engine: str, lang: str) -> str:
    harvard = sr.AudioFile(audio_path)
    with harvard as source:
        try:
            audio = r.record(source)
        except sr.audioop.error as e:
            print(f'sr.audioop.error: {e}')
            return ''
    try:
        if engine == 'google':
            return r.recognize_google(audio, language=lang)
        elif engine == 'sphinx':
            return r.recognize_sphinx(audio, language=lang)
    except sr.UnknownValueError:
        return ''
