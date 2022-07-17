import azure.cognitiveservices.speech as speechsdk
import requests as req
import urllib


def from_file():
    speech_config = speechsdk.SpeechConfig(subscription="d5c54572157843cb9d133eb22c92944b", region="koreacentral")
    audio_input = speechsdk.AudioConfig(filename="fb.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    result = speech_recognizer.recognize_once_async().get()
    print(result.text)


def down_file():
    URL = 'https://ticket.interpark.com' \
          '/CommonAPI/Captcha/x?v=en&t=u2wRmo4CWlZLO1gyt3zs2HHN8gIjbTNAU9gLApCJm4E%3D&p1=1645631528653'
    file = req.get(URL)

    open('audio.wav', 'wb').write(file.content)


def down_file2():
    urllib.request.urlretrieve("http://ticket.interpark.com/CommonAPI/Captcha/GetCaptchaAudio?v=en&t=ZdWKvH8M4PQsCApowsu40iemi7HSqQGRa%2BoKMpt9cWY%3D&p1=1645632154827",
                               "fb.wav")

from_file()
# down_file2()