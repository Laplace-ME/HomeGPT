import speech_recognition as sr
import sys

def translate_voice_into_text(langue: str ='fr-FR'):
    """_summary_

    Args:
        langue (str, optional): _description_. Defaults to 'fr-FR'.
    """
    recognizer = sr.Recognizer()
    source = sr.Microphone()

    while True:
        print("Parlez maintenant...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

        try:
            print("Transcription : " + recognizer.recognize_google(audio, language=langue))
        except sr.UnknownValueError:
            print("Impossible de comprendre l'audio")
        except sr.RequestError as e:
            print(f"Erreur lors de la requête à l'API Google Speech Recognition : {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        translate_voice_into_text(sys.argv[1])
    translate_voice_into_text()
