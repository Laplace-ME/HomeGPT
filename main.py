import speech_recognition as sr
from dotenv import load_dotenv
import openai
import pyttsx3
import sys
import os
import time

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

HISTORIQUE = []

# "cuisine": "https://www.marmiton.org/recettes/",
# "bricolage": "https://www.leroymerlin.fr/v3/p/idees-bricolage/",
# "jardinage": "https://www.jardiland.com/idees-conseils/idees-jardin/",
# "sport": "https://www.decathlon.fr/C-10851-idees-sport",
# "informatique": "https://www.cours-gratuit.com/informatique",
# "mécanique": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", // it's a rickroll

EXPERTS = {
    "cuisine": os.getenv("CUISINE_PROMPT"),
    "bricolage": os.getenv("BRICOLAGE_PROMPT"),
    "jardinage": os.getenv("JARDINAGE_PROMPT"),
    "sport": os.getenv("SPORT_PROMPT"),
    "informatique": os.getenv("INFORMATIQUE_PROMPT"),
    "mécanique": os.getenv("MECANIQUE_PROMPT"),
}

CURRENT_PROMPT = PROMPT

COMMANDS = {
    "bonjour": "Bonjour, comment allez-vous ?",
    "ça va": "Je vais bien, merci !",
    "merci": "Je vous en prie !",
    "au revoir": "Au revoir, à bientôt !",
    "quelle heure est-il": "Il est " + time.strftime("%H:%M"),
    "quelle est la date": "Nous sommes le " + time.strftime("%d/%m/%Y"),
    "quelle est la météo": "Il fait beau et chaud",
    "quelle est la température": "Il fait 25 degrés",
    "dis-moi une blague": "Qu'est-ce qui est jaune et qui attend ? Jonathan !",
    "discute avec moi": "Je ne sais pas quoi dire",
    "raconte-moi une histoire": "Il était une fois...",
    "fais-moi une recette de cuisine": REPONSE,
    "help": "Je peux vous donner l'heure, la date, la météo, la température, vous raconter une blague ou une histoire, ou vous faire une recette de cuisine",
    "donne moi mon historique": HISTORIQUE,
    "close": "Au revoir, à bientôt !",
    "j'aimerais parler à un expert en": "Je ne suis pas un expert en {0}, mais je peux vous aider à trouver un expert en {0}.",
    "redevient mon assistant": "Je suis de nouveau votre assistant !",
    "redevient normal": "Je suis de nouveau normal !",
}

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

def text_to_speech(text: str, lang: str ='fr'):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Use the system voice (you can change the index to select a different voice)
    engine.setProperty('voice', lang)
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
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        while True:
            print("Parlez maintenant...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)

            try:
                transcription = recognizer.recognize_google(audio, language=langue).lower()
                if transcription.startswith("j'aimerais parler à un expert en"):
                    if transcription.split("en ")[1] not in EXPERTS.keys():
                        print("Transcription : " + transcription)
                        text_to_speech("Je ne suis pas un expert en " + transcription.split("en ")[1] + ", mais je peux vous aider à trouver un expert en " + transcription.split("en ")[1] + ".")
                        continue
                    CURRENT_PROMPT = EXPERTS.get(transcription.split("en ")[1])
                    print("Nouveau prompt : " + CURRENT_PROMPT)
                    text_to_speech("Je vous mets en relation avec un expert en " + transcription.split("en ")[1] + ".")
                    continue
                elif transcription.startswith("redevient mon assistant") or transcription.startswith("redevient normal"):
                    CURRENT_PROMPT = PROMPT
                    print("Nouveau prompt : " + CURRENT_PROMPT)
                    text_to_speech("Je suis de nouveau votre assistant !")
                    continue
                if COMMANDS.get(transcription) is not None:
                    if transcription == "discute avec moi":
                        HISTORIQUE.append(transcription)
                    elif transcription == "close":
                        print("Commande : " + transcription)
                        text_to_speech(COMMANDS.get(transcription))
                        break
                    print("Commande : " + transcription)
                    text_to_speech(COMMANDS.get(transcription))
                    continue

                print("Transcription : " + transcription)
                # response = get_openai_response(CURRENT_PROMPT, transcription)
                response = "Je n'ai pas compris"
                print("Réponse : " + response)
                text_to_speech(response, langue.split("-")[0])
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
