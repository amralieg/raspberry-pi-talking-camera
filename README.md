# Raspberry PI multi-lingual talking camera using Google Cloud AI
Using a camera module mounted on top of the Raspberry PI 4, this project will capture an image, send it to Google Cloud Vision for recognition, receive the response, send it to Google translate to translate it to diffrent languages and finally send it to Google Cloud text to speach to say the content.

It uses OKDO Raspbperry PI 4 Kit [https://www.okdo.com/p/okdo-raspberry-pi-4-4gb-model-b-starter-set/] and Camera Module [https://uk.rs-online.com/web/p/video-modules/9132673]

## Prerequisites
### to run this project, you'll need to do the following steps:
1. Have a google cloud platform account, you can create one for free.
2. Enable the Google Cloud Vision API and the Google Cloud Text to Speech API
3. Install python client liberaies
	1. pip3 install --upgrade google-cloud-texttospeech
	2. pip3 install --upgrade google-cloud-vision
	3. pip3 install --upgrade google-cloud-translate
4. create service account file (see this link)[https://cloud.google.com/docs/authentication/getting-started]
5. SET GOOGLE_APPLICATION_CREDENTIAL environment variable to the path of the service account file that you downloaded
6. Run python script

