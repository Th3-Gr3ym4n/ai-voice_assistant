import openai
import speech_recognition as sr
import pyttsx3
import time
import env as ev

# Inicializar OpenAI API
openai.api_key = ev.OPEN_AI_KEY

# Inicializar el motor de texto a voz
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language="es")
    except sr.UnknownValueError:
        print("Señor, no se pudo entender el audio.")
    except sr.RequestError as e:
        print(f"Señor, ocurrió un error en la solicitud de reconocimiento de voz: {e}")

def generate_response(prompt):
    role = "Actua como J.A.R.V.I.S el asistente de Tony Stark, responde con humor y sarcasmo y dirígete siempre a mi llamándome señor"
    #role = "Actua como el Doctor House. Responde con sarcasmo y humor ácido. Debes llamarme cuando quieras dirigirte a mi con el nombre de Fito."
    full_prompt = f"Role: {role}\n{prompt}"
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=full_prompt,
            max_tokens=4000,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response["choices"][0]["text"]
    except Exception as e:
        print(f"Señor, hubo un error al generar la respuesta: {e}")
        return ""

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        print("Di 'hola', 'claro', o 'me matas' para empezar a grabar")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            recognizer.pause_threshold = 2
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio, language="es")
                print(transcription)
                if any(keyword in transcription.lower() for keyword in ["hola", "claro", "me matas"]):
                    filename = "input.wav"
                    print("Ya puedes interactuar con J.A.R.V.I.S")
                    audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                    with open(filename, "wb") as f:
                        f.write(audio.get_wav_data())
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"Yo: {text}")
                        response = generate_response(text)
                        if response:
                            print(f"J.A.R.V.I.S dice: {response}")
                            speak_text(response)
            except sr.UnknownValueError:
                print("Señor, no se pudo entender el audio.")
            except sr.RequestError as e:
                print(f"Señor, ocurrió un error en la solicitud de reconocimiento de voz: {e}")
            except Exception as e:
                print(f"Señor, hubo un error inesperado: {e}")

if __name__ == "__main__":
    main()
