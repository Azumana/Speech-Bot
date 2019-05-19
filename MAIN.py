import azure.cognitiveservices.speech as speechsdk
import TEXTTOSPEECH as ttsp
import CHATBOT as bot
import MEMORY


def getinfo():
    """Use to get speech key and other private data"""
    pass


def getstart():
    """When program starts, chatbot says hello to people"""
    botvoice = ttsp.TextToSpeech(speech_key, "Bonjour, je suis Captèn botte, " 
                                             " ton assistant personnel. En quoi puis-je t'aider ?")
    botvoice.get_token()
    botvoice.save_audio("getstart.wav")
    botvoice.read_audio("getstart.wav")


def nomatch():
    """Use when the record didn't work"""
    botvoice = ttsp.TextToSpeech(speech_key, "Je n'ai pas compris ta demande. Peux-tu répéter s'il te plaît ?")
    botvoice.get_token()
    botvoice.save_audio("nomatch.wav")
    botvoice.read_audio("nomatch.wav")


def sth_else():
    """Use to ask people for another question after chatbot's answer"""
    botvoice = ttsp.TextToSpeech(speech_key, "Est-ce que tu as d'autres questions ?")
    botvoice.get_token()
    botvoice.save_audio("sth_else.wav")
    botvoice.read_audio("sth_else.wav")


def byebye():
    """Use to say good bye when conversation loop ends"""
    botvoice = ttsp.TextToSpeech(speech_key, "J'espère t'avoir aidé. Bonne journée et à bientôt !")
    botvoice.get_token()
    botvoice.save_audio("byebye.wav")
    botvoice.read_audio("byebye.wav")


if __name__ == '__main__':

    speech_key = "speech_key"
    service_region = "service_region"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key,
                                           region=service_region,
                                           speech_recognition_language='fr-FR')

    # Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    # program starts
    getstart()
    record = speech_recognizer.recognize_once()
    # create an object to stock informations
    mem = MEMORY.Memory(record)

    # Use a loop for the conversation
    while "au revoir." not in record.text.lower():

        # Check record
        if record.reason == speechsdk.ResultReason.RecognizedSpeech:
            question = record.text.rstrip(".")
            # get the answer from the chatbot program
            answer = bot.bobot(question, mem)

            # check if chatbot already answered to this question :-)
            if mem.answer.count(answer) > 1:
                botres = ttsp.TextToSpeech(speech_key, "J'ai déjà répondu à cette question !")
                botres.get_token()
                botres.save_audio('again.wav')
                botres.read_audio('again.wav')

            else:
                botres = ttsp.TextToSpeech(speech_key, answer)
                botres.get_token()
                botres.save_audio('answer.wav')
                botres.read_audio('answer.wav')

            # ask for another question
            sth_else()

        else:
            # say that the program didn't understand the record
            nomatch()

        # for a new record in the loop
        record = speech_recognizer.recognize_once()

    byebye()