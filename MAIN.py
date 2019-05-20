import argparse
import azure.cognitiveservices.speech as speechsdk
import TEXTTOSPEECH as ttsp
import CHATBOT as bot
import MEMORY


def get_config():
    """Use to get speech key and other private data"""
    parser = argparse.ArgumentParser()
    parser.add_argument("configFile")
    args = parser.parse_args()
    return args


def getstart():
    """When program starts, chatbot says hello to people"""
    botvoice = ttsp.TextToSpeech(speech_key, service_region, "Bonjour, je suis Captèn botte, "
                                                             " ton assistant personnel. En quoi puis-je t'aider ?")
    botvoice.get_token()
    botvoice.save_audio("getstart.wav")
    botvoice.read_audio("getstart.wav")


def nomatch():
    """Use when the record didn't work"""
    botvoice = ttsp.TextToSpeech(speech_key, service_region,
                                 "Je n'ai pas compris ta demande. Peux-tu répéter s'il te plaît ?")
    botvoice.get_token()
    botvoice.save_audio("nomatch.wav")
    botvoice.read_audio("nomatch.wav")


def sth_else():
    """Use to ask people for another question after chatbot's answer"""
    botvoice = ttsp.TextToSpeech(speech_key, service_region, "Est-ce que tu as d'autres questions ?")
    botvoice.get_token()
    botvoice.save_audio("sth_else.wav")
    botvoice.read_audio("sth_else.wav")


def byebye():
    """Use to say good bye when conversation loop ends"""
    botvoice = ttsp.TextToSpeech(speech_key, service_region, "J'espère t'avoir aidé. Bonne journée et à bientôt !")
    botvoice.get_token()
    botvoice.save_audio("byebye.wav")
    botvoice.read_audio("byebye.wav")


if __name__ == '__main__':

    configInfo = get_config()
    config = bot.openjson(configInfo.configFile)

    speech_key = config["speech_key"]
    service_region = config["service region"]

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
            print("q = ", question)
            # get the answer from the chatbot program
            answer = bot.bobot(question, mem)
            print(answer)

            # check if chatbot already answered to this question :-)
            if mem.answer.count(answer) > 1:
                botres = ttsp.TextToSpeech(speech_key, service_region, "J'ai déjà répondu à cette question !"
                                                                       "veux-tu vraiment que je me répète ?")
                botres.get_token()
                botres.save_audio('again.wav')
                botres.read_audio('again.wav')

                recordbis = speech_recognizer.recognize_once()
                print("recordbis = ", recordbis)
                if "s'il te plaît" in recordbis.text.lower():
                    print("OUI !")
                    botres = ttsp.TextToSpeech(speech_key, service_region, answer)
                    botres.get_token()
                    botres.save_audio('answer.wav')
                    botres.read_audio('answer.wav')


            else:
                botres = ttsp.TextToSpeech(speech_key, service_region, answer)
                botres.get_token()
                botres.save_audio('answer.wav')
                botres.read_audio('answer.wav')

            # ask for another question
            if not answer.endswith("?"):
                sth_else()

        else:
            # say that the program didn't understand the record
            nomatch()

        # for a new record in the loop
        record = speech_recognizer.recognize_once()

    byebye()
