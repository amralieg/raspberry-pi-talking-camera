# python-google-cloud-vision
this simple python script will show you how to send an image to google cloud vision and get the response back and sends it to google cloud text to speech to tell the content of the image.

## Running the script
### to run this script, you'll need to do the following steps:
	1. Have a google cloud platform account
	2. Enable the Google Cloud Vision API and the Google Cloud Text to Speech API
	3. Install python client liberaies
		1. pip install --upgrade google-cloud-texttospeech
		2. pip install --upgrade google-cloud-vision
	4. create service account file [see this link](https://cloud.google.com/docs/authentication/getting-started)
	5. SET GOOGLE_APPLICATION_CREDENTIAL environment variable to the path of the service account file that you downloaded
	6. Run python script

