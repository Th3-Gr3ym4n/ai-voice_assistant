## AI JARVIS Text-to-Speech Assistant Lab

This Python script provides a speech recognition and text-to-speech assistant. It uses the OpenAI API to generate responses and the Google Speech Recognition library to transcribe audio.

This is a lab for my own investigation and learning.
### Installation

To use this script, you will need to install the following dependencies:

  * OpenAI
  * Speech Recognition
  * PyTTSx3
  * dotenv

You can install these dependencies using pip:

```
pip install openai speech_recognition pyttsx3 dotenv
```

### Configuration

You will need to create a .env file with the following environment variables:

  * `OPEN_API_KEY`: Your OpenAI API key
  * `GPT_MODEL`: The OpenAI model to use (default: `gpt-3.5-turbo`)
  * `MAX_TOKENS`: The maximum number of tokens to generate in a response (default: `1000`)
  * `TEMPERATURE`: The temperature of the response (default: `0.7`)
  * `JARVIS_PROMPT`: The prompt used to generate responses (default: `You are JARVIS, the assistant of Tony Stark. Respond with humor and sarcasm, and direct yourself to the user as 'señor'.`)
  * `ACTIVATION_KEYWORDS`: The keywords used to activate the assistant (default: `hola,claro,me matas`)
  * `PAUSE_THRESHOLD`: The pause threshold in seconds (default: `1.0`)
  * `AUDIO_FILE`: The name of the audio file to save recordings to (default: `input.wav`).

### Usage

To use the assistant, simply run the script and say the activation keyword. The assistant will then start listening for your commands.

Here are some examples of commands you can give:

  * "J.A.R.V.I.S, what's the weather like?"
  * "J.A.R.V.I.S, translate this sentence for me: 'The quick brown fox jumps over the lazy dog.'"
  * "J.A.R.V.I.S, create a Python script that prints the numbers from 1 to 10."
  * "J.A.R.V.I.S, tell me a joke."

The assistant will respond to your commands using the OpenAI API. You can also use the assistant to transcribe audio files. To do this, simply say the command "J.A.R.V.I.S, transcribe this audio file." The assistant will then transcribe the audio file and print the results.

### Documentation

This script is intended for use with the OpenAI API. The OpenAI API is a paid service, so you will need to sign up for an account before you can use it. You can find more information about the OpenAI API here: [https://openai.com/api/](https://www.google.com/url?sa=E&source=gmail&q=https://openai.com/api/)

### License

This script is licensed under the MIT License. You are free to modify and distribute the script as you see fit, but you must include the original copyright notice and license text.
