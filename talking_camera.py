from gpiozero import Button
from signal import pause
from time import sleep
from picamera import PiCamera
import pygame
import random

from google.cloud import vision
from google.cloud import texttospeech
from google.cloud import translate_v2 as translate

SHUTTER = "GPIO8"
REPLAY = "GPIO7"
photo_path = '/tmp/photo.jpg'
sound_path = '/tmp/sound.wav'

greetings_list = [
    "what a nice ", "that's a cool ", "I like this ",
    "nice ", "this is a ", "looks like a ", "wow, that's a very cool "
]

target_languages = {
    "fr ",  ## french
    "es ",  ## spanish
    "it",  ## italian
    "ar",  ## arabic
    "zh"  ## chinese
}


def take_photo(photo_path):
    camera.capture(photo_path)


def play_sound(sound_path):
        recording = pygame.mixer.Sound(sound_path)
        recording.play()


def replay():
    play_sound(sound_path)


def say_it(text, file):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-GB',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    # Set audio file format to Wav
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)
    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    with open(file, 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file ' + file)


def see_it(file) -> 'res':
    res = ""
    with open(file, "rb") as imageFile:
        client = vision.ImageAnnotatorClient()
        response = client.annotate_image({
            'image': {'content': imageFile.read()},
            'features': [{'type': vision.enums.Feature.Type.LABEL_DETECTION}]
        })
        res = "sorry, I can't see that quite clearly"
        if len(response.label_annotations) > 0:
            res = response.label_annotations[0].description
    print(res)
    return res


def translate_it(text, target_language):
    translate_client = translate.Client()
    # target_language to be selected from target_languages list above
    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language)

    print(u'Text: {}'.format(result['input']))
    print(u'Translation: {}'.format(result['translatedText']))
    print(u'Detected source language: {}'.format(
        result['detectedSourceLanguage']))
    return result['translatedText']


def action():
    global sound_path
    take_photo(photo_path)
    description = see_it(photo_path)
    if description == 'Rat':
        sound_path = 'sound/its-a-rat.wav'
    else:
        sound_path = '/tmp/sound.wav'
        description = random.choice(greetings_list) + description
        say_it(description, sound_path)
    play_sound(sound_path)


pygame.init()
shutter_button = Button(SHUTTER)
replay_button = Button(REPLAY)
camera = PiCamera()
camera.resolution = (1024, 768)

camera.start_preview()
sleep(2)  # Camera warm-up time

shutter_button.when_pressed = action
replay_button.when_released = replay

pause()
