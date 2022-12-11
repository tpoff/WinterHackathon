# Speak-2-Me
## Project Description
Prompt users to speak any question such as "Tell me something about Dallas". The application will perform NLP to extract subject and intend. User command will be used to search for appropriate Wiki, Youtube, and Flickr content. Text result will be spoken to user as response.

## Installation Instruction
### Install Python Libraries
```
$ brew install portaudio
$ pip install -r requirements.txt
$ conda install --file conda_requirements.txt
```

### Setup Flask
```
$ export FLASK_APP=FlaskApp
$ export FLASK_ENV=development
$ flask run
```

## Technical Links

### YouTube API
- https://medium.com/mcd-unison/youtube-data-api-v3-in-python-tutorial-with-examples-e829a25d2ebd
- https://developers.google.com/youtube/v3/getting-started
- https://www.python-engineer.com/posts/youtube-data-api-01/

### Flickr API
- https://www.flickr.com/services/api/
- https://joequery.me/code/flickr-api-image-search-python/
- https://code.google.com/archive/p/python-flickr-api/wikis/Tutorial.wiki

### Wiki API
- https://towardsdatascience.com/wikipedia-api-for-python-241cfae09f1c
- https://www.geeksforgeeks.org/wikipedia-module-in-python/
- https://www.jcchouinard.com/wikipedia-api/

### Twitter API
- https://towardsdatascience.com/an-extensive-guide-to-collecting-tweets-from-twitter-api-v2-for-academic-research-using-python-3-518fcb71df2a
- https://developer.twitter.com/en/docs/twitter-api/tools-and-libraries/v2
- https://www.jcchouinard.com/twitter-api/

### Hugging Face API
- https://huggingface.co/docs/api-inference/quicktour
- https://github.com/huggingface/hfapi
- https://huggingface.co/docs/huggingface_hub/package_reference/hf_api

### AssemblyAI API
- https://www.assemblyai.com/docs/#introduction
- https://www.assemblyai.com/docs/walkthroughs#submitting-files-for-transcription
- https://www.assemblyai.com/docs/core-transcription#automatic-punctuation-and-casing
- https://www.assemblyai.com/docs/walkthroughs#specifying-a-language
- https://www.assemblyai.com/blog/real-time-speech-recognition-with-python/

### Audio
- https://www.geeksforgeeks.org/create-a-voice-recorder-using-python/
- https://realpython.com/playing-and-recording-sound-python/
- https://python-sounddevice.readthedocs.io/en/0.3.7/

### Flask
- https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3#prerequisites
- https://www.tutorialspoint.com/flask/flask_application.htm


---
*Copyright (c) 2022.* [AssemblyAI Hackathon](https://hackathon.assemblyai.com/)