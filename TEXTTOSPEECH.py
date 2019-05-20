import os, requests
from xml.etree import ElementTree


class TextToSpeech(object):

    def __init__(self, subscription_key, region, SpeechText):
        self.subscription_key = subscription_key
        self.tts = SpeechText
        self.region = region
        self.access_token = None

    def get_token(self):
        fetch_token_url = "https://" + self.region + ".api.cognitive.microsoft.com/sts/v1.0/issuetoken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def save_audio(self, wavName):
        base_url = 'https://' + self.region + '.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'YOUR_RESOURCE_NAME'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'fr-FR')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'fr-FR')
        voice.set('name', 'Microsoft Server Speech Text to Speech Voice (fr-FR, Julie, Apollo)')
        voice.text = self.tts
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)
        if response.status_code == 200:
            with open(wavName, 'wb') as audio:
                audio.write(response.content)
                print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")

        else:
            print("\nStatus code: " + str(
                response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")

    def read_audio(self, wavName):
        os.system("aplay " + wavName)
