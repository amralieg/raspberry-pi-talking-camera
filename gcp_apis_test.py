import random

from google.cloud import vision
from google.cloud import texttospeech

greetings_list = [
    "what a nice ", "that's a cool ", "I like this ",
    "nice ", "this is a ", "looks like a ", "wow, that's a very cool "
]


def see_it(file):
    res = ""
    with open(file, "rb") as imageFile:
        client = vision.ImageAnnotatorClient()
        response = client.annotate_image({
            'image': {'content': imageFile.read()},
            'features': [{'type': vision.enums.Feature.Type.LABEL_DETECTION}]
        })

        res = "sorry, I can't see that quiet clearly"
        if len(response.label_annotations) > 0:
            res = random.choice(greetings_list) + response.label_annotations[0].description
    print(res)
    return res


def say_it(text, file):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    with open(file, 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file ' + file)


def see_it_say_it(in_image, out_mp3):
    description = see_it(in_image)
    say_it(description, out_mp3)

# capture the camera input as jpeg and pass it to this function along with the file where you want the
# output audio to be stored.


def main():
    see_it_say_it("D:\\tint1.jpg", "D:\\output.mp3")


if __name__ == "__main__":
    main()
