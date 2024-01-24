import openai
import speech_recognition as sr
import pyttsx3
import time
import env as ev


# Initialize OpenAI API
openai.api_key =ev.OPEN_AI_KEY
print(openai.api_key)
# Initialize the text to speech engine 
engine=pyttsx3.init()


def transcribe_audio_to_test(filename):
    recogizer=sr.Recognizer()
    with sr.AudioFile(filename)as source:
        audio=recogizer.record(source) 
    try:
        return recogizer.recognize_google(audio, language="es")
    except:
        print("Señor, no entiendo que ha podido pasar. Que ha tocado?")

def generate_response(prompt):
    role = "Actua como J.A.R.V.I.S el asistente de Tony Stark, responde con humor y sarcasmo y dirígete siempre a mi llmándome señor"
    #role = "Actua como una persona con un CI alto. Responde siempre llamándome FITO pero con humor sarcástico."
    full_prompt = f"Role: {role}\n{prompt}"
    response= openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=full_prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response ["choices"][0]["text"]

# Set Spanish voice for text-to-speech engine
voices = engine.getProperty('voices')
spanish_voice = None
for voice in voices:
    if "spanish" in voice.languages:
        spanish_voice = voice.id
if spanish_voice is not None:
    engine.setProperty('voice', spanish_voice)

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        #Waith for user say "genius"
        print("Di 'hola, claro o me matas' para empezar a grabar")
        with sr.Microphone() as source:
            recognizer=sr.Recognizer()
            audio=recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio, language="es")
                print(transcription)
                if "claro" in transcription.lower() or "hola" in transcription.lower() or "me matas" in transcription.lower(): #if transcription.lower()=="claro":
                    #record audio
                    filename ="input.wav"
                    print("Ya puedes interactuar con J.A.R.V.I.S")
                    with sr.Microphone() as source:
                        recognizer=sr.Recognizer()
                        source.pause_threshold=1
                        audio=recognizer.listen(source,phrase_time_limit=None,timeout=None)
                        with open(filename,"wb")as f:
                            f.write(audio.get_wav_data())
                    #transcript audio to test 
                    text=transcribe_audio_to_test(filename)
                    if text:
                        print(f"Yo {text}")
                        
                        #Generate the response
                        response = generate_response(text)
                        print(f"J.A.R.V.I.S dice: {response}")
                            
                        #read resopnse using GPT3
                        speak_text(response)
            except Exception as e:
                
                print("señor, me temo que hubo un error : {}".format(e))
if __name__=="__main__":
    main()