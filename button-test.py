from gpiozero import Button
from signal import pause
from time import sleep
from picamera import PiCamera
import pygame
import random

from google.cloud import vision
from google.cloud import texttospeech

SHUTTER = "GPIO8"
REPLAY = "GPIO7"
photo_path = '/tmp/photo.jpg'
sound_path = '/tmp/sound.wav'
text = "Watch out for Daleks"


def take_photo():
    camera.capture(photo_path)
    say_it(text, sound_path)
    #play_sound('dalek')
    play_sound(None)


def play_sound(description):
    global sound_path
    if description == "dalek":
        sound_path = 'sound/exterminate.wav'
        recording = pygame.mixer.Sound(sound_path)
        for _ in range(3):
            recording.play()
            sleep(2)
    else:
        sound_path = '/tmp/sound.wav'
        recording = pygame.mixer.Sound(sound_path)
        recording.play()


def replay():
        recording = pygame.mixer.Sound(sound_path)
        recording.play()


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


pygame.init()
shutter_button = Button(SHUTTER)
replay_button = Button(REPLAY)
camera = PiCamera()
camera.resolution = (1024, 768)

camera.start_preview()
sleep(2)  # Camera warm-up time

shutter_button.when_pressed = take_photo
replay_button.when_released = replay

pause()
