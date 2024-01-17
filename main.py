import speech_recognition as sr
from dotenv import load_dotenv
import openai
import sys
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_TOKEN")
PROMPT = os.getenv("OPENAI_PROMPT")

def get_openai_response(prompt: str, text: str) -> str:
    """_summary_

    Args:
        prompt (str): _description_
        text (str): _description_

    Returns:
        str: _description_
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"{text}"}
            ],
            temperature=0.7,
        )
        print(response)
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Erreur lors de la requête à l'API OpenAI : {e}")
        return "Je n'ai pas compris"

def translate_voice_into_text(langue: str ='fr-FR'):
    """_summary_

    Args:
        langue (str, optional): _description_. Defaults to 'fr-FR'.
    """
    # recognizer = sr.Recognizer()

    # with sr.Microphone() as source:
    while True:
        # print("Parlez maintenant...")
        # recognizer.adjust_for_ambient_noise(source, duration=0.5)
        # audio = recognizer.listen(source)

        try:
            # transcription = recognizer.recognize_google(audio, language=langue)
            transcription = " bonsoir fais-moi une recette de cuisine avec des tomates et des œufs"
            print("Transcription : " + transcription)
            response = get_openai_response(PROMPT, transcription)
            print("Réponse : " + response)
        except sr.UnknownValueError:
            print("Impossible de comprendre l'audio")
        except sr.RequestError as e:
            print(f"Erreur lors de la requête à l'API Google Speech Recognition : {e}")

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            translate_voice_into_text(sys.argv[1])
        translate_voice_into_text()
    except KeyboardInterrupt:
        print("\r\nFin du programme")
