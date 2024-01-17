import speech_recognition as sr
from dotenv import load_dotenv
import openai
import pyttsx3
import sys
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_TOKEN")
PROMPT = os.getenv("OPENAI_PROMPT")

TRANSCRIPTION= """\
bonsoir fais-moi une recette de cuisine avec des tomates et des œufs
"""

REPONSE = """\
Ingrédients :

    4 œufs
    2 tomates mûres, coupées en dés
    1/2 oignon, haché
    1 poivron rouge, coupé en dés
    1/2 tasse de fromage râpé (au choix)
    Sel et poivre, selon votre goût
    Herbes fraîches (persil, ciboulette), hachées

Instructions :

    Dans un bol, battez les œufs et assaisonnez-les avec du sel et du poivre.

    Dans une poêle antiadhésive, faites revenir l'oignon et le poivron rouge à feu moyen jusqu'à ce qu'ils soient tendres.

    Ajoutez les tomates coupées en dés à la poêle et laissez-les mijoter pendant quelques minutes jusqu'à ce qu'elles libèrent leur jus.

    Versez les œufs battus sur les légumes dans la poêle. Remuez doucement pour mélanger les ingrédients.

    Lorsque les bords de l'omelette commencent à se solidifier, saupoudrez le fromage râpé sur la moitié de l'omelette.

    Une fois que l'omelette est bien prise, pliez-la en deux pour recouvrir le fromage.

    Laissez cuire encore quelques minutes jusqu'à ce que le fromage soit fondu et que l'omelette soit bien cuite.

    Saupoudrez d'herbes fraîches hachées avant de servir.

Voilà, une omelette aux tomates et aux œufs délicieuse et rapide à préparer ! J'espère que vous apprécierez ce plat. Si vous avez d'autres préférences ou des ingrédients spécifiques en tête, n'hésitez pas à me le faire savoir !
"""

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

def text_to_speech(text: str):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Get the system voices
    voices = engine.getProperty('voices')

    # Use the system voice (you can change the index to select a different voice)
    engine.setProperty('voice', voices[0].id)

    # Set the rate of speech (optional)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)  # You can adjust the rate as needed

    # Convert and speak the text
    engine.say(text)

    # Wait for the speech to finish
    engine.runAndWait()


def translate_voice_into_text(langue: str ='fr-FR'):
    """_summary_

    Args:
        langue (str, optional): _description_. Defaults to 'fr-FR'.
    """
    # recognizer = sr.Recognizer()

    # with sr.Microphone() as source:
    while True:
        print("Parlez maintenant...")
        # recognizer.adjust_for_ambient_noise(source, duration=0.5)
        # audio = recognizer.listen(source)

        try:
            # transcription = recognizer.recognize_google(audio, language=langue)
            transcription = TRANSCRIPTION
            print("Transcription : " + transcription)
            # response = get_openai_response(PROMPT, transcription)
            response = REPONSE
            print("Réponse : " + response)
            text_to_speech(response)
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
