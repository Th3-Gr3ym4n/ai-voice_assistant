from openai import OpenAI
import speech_recognition as sr
import pyttsx3
import time
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPEN_API_KEY'))

# Initialize text-to-speech engine
engine = pyttsx3.init()

def transcribe_audio(filename: str) -> Optional[str]:
    """Transcribe audio file to text using Google Speech Recognition in Spanish"""
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio, language="es")
    except sr.UnknownValueError:
        print("Señor, no se pudo entender el audio.")
        return None
    except sr.RequestError as e:
        print(f"Señor, ocurrió un error en la solicitud de reconocimiento de voz: {e}")
        return None

def generate_response(prompt: str, conversation_history: list) -> str:
    """Generate response using OpenAI's GPT model with JARVIS personality"""
    system_message = os.getenv('JARVIS_PROMPT', 
        "Eres JARVIS, el asistente de Tony Stark. Responde con humor y sarcasmo, y dirígete siempre al usuario como 'señor'.")
    
    try:
        messages = [{"role": "system", "content": system_message}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=os.getenv('GPT_MODEL', 'gpt-3.5-turbo'),
            messages=messages,
            max_tokens=int(os.getenv('MAX_TOKENS', '1000')),
            temperature=float(os.getenv('TEMPERATURE', '0.7')),
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Señor, hubo un error al generar la respuesta: {e}")
        return "Lo siento señor, pero parece que mis circuitos están un poco confundidos en este momento."

def speak_text(text: str) -> None:
    """Convert text to speech"""
    try:
        engine.say(text)
        engine.runAndWait()
        # Add a small delay after speaking to prevent audio overlap
        time.sleep(0.5)
    except Exception as e:
        print(f"Señor, hubo un error al reproducir el audio: {e}")

def process_voice_command(recognizer: sr.Recognizer, source: sr.Microphone) -> Optional[str]:
    """Process voice command and return transcription"""
    try:
        print("Escuchando...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        return recognizer.recognize_google(audio, language="es")
    except sr.WaitTimeoutError:
        print("No se detectó ningún comando.")
        return None
    except (sr.UnknownValueError, sr.RequestError) as e:
        print(f"Señor, hubo un error al procesar el comando de voz: {e}")
        return None

def main() -> None:
    """Main execution loop"""
    # Get activation keywords from environment variables or use defaults
    activation_keywords = os.getenv('ACTIVATION_KEYWORDS', 'hola,claro,me matas').split(',')
    exit_keyword = "adios"
    audio_file = os.getenv('AUDIO_FILE', 'input.wav')
    
    recognizer = sr.Recognizer()
    conversation_history = []
    is_active = False
    
    print("Di 'hola', 'claro', o 'me matas' para empezar a grabar")
    
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                recognizer.pause_threshold = float(os.getenv('PAUSE_THRESHOLD', '1.0'))
                
                if not is_active:
                    command = process_voice_command(recognizer, source)
                    if not command:
                        continue
                        
                    print(f"Comando detectado: {command}")
                    
                    if any(keyword in command.lower() for keyword in activation_keywords):
                        is_active = True
                        print("Ya puedes interactuar con J.A.R.V.I.S")
                        speak_text("A sus órdenes señor, ¿en qué puedo ayudarle?")
                
                while is_active:
                    print("Escuchando su orden...")
                    try:
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                        
                        with open(audio_file, "wb") as f:
                            f.write(audio.get_wav_data())
                        
                        if text := transcribe_audio(audio_file):
                            print(f"Yo: {text}")
                            
                            if exit_keyword in text.lower():
                                print("Finalizando conversación...")
                                speak_text("Hasta luego señor, que tenga un buen día.")
                                is_active = False
                                conversation_history.clear()
                                break
                                
                            if response := generate_response(text, conversation_history):
                                print(f"J.A.R.V.I.S dice: {response}")
                                speak_text(response)
                                # Add the interaction to conversation history
                                conversation_history.append({"role": "user", "content": text})
                                conversation_history.append({"role": "assistant", "content": response})
                                
                    except sr.WaitTimeoutError:
                        print("No se detectó ninguna orden. ¿Desea continuar?")
                        speak_text("Señor, ¿sigue ahí?")
                        continue
                    except Exception as e:
                        print(f"Error en el bucle de conversación: {e}")
                        is_active = False
                        break
                        
        except KeyboardInterrupt:
            print("\nPrograma terminado por el usuario.")
            break
        except Exception as e:
            print(f"Error general: {e}")
            continue

if __name__ == "__main__":
    main()
