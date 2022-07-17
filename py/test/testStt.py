import azure.cognitiveservices.speech as speechsdk

def from_file():
    speech_config = speechsdk.SpeechConfig(subscription="d5c54572157843cb9d133eb22c92944b", region="koreacentral")
    audio_input = speechsdk.AudioConfig(filename="GetCaptchaAudio.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    result = speech_recognizer.recognize_once_async().get()
    print(result.text)

from_file()