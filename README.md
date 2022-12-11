# Speak-2-Me
[![Watch Video Presentation](https://i.ytimg.com/an_webp/318jiesm8wo/mqdefault_6s.webp?du=3000&sqp=COyk2JwG&rs=AOn4CLAWTtpyjfSu38pcbCNUl4wJ8ystqg)](https://youtu.be/318jiesm8wo)

## Inspiration
Recent advancements in NLP and Unity make interactive avatars more accessible than ever. We believe that interactive AI that users can simply have a conversation with to answer their questions and complete their requests will be the next wave of customer service. We were inspired by videos from companies such as Nvidia showcasing the possibilities of these AI and decided to build one ourselves using the latest in NLP.

## Project Description
Our bot can answer questions about locations on Earth. Users can naturally speak their questions and requests to the bot and get answers spoken back to them. If a user asks "What is the history of Washington DC" our ai will be able to deliver a brief summary. It can also deliver images and youtube videos pertaining to the topic being discussed. The digital avatar also provides visual feedback and increases the interaction with the user, users can see the bot speaking back to them. 

The basic feedback loop is the user speaks into the microphone, the audio information is transcribed in real time using Assembly.AI technology, the text output is then run through an NLP process to extract the subject of the querry (where) and the question (what). Using those pieces of information the bot searches wikipedia, flickr and youtube for relevant information, constructs an html to present the information and then speaks the information it found online back to the user, as well as display the visual results. 

## How we built it
We started with the workflow and found technology to help accomplish our goals. Unity was chosen as the visual output layer, Python as the driving force of the backend due to the ease of use with ML technologies. The automatic speech recognition was accomplished through Assembly.AI, while the NLP was done through a combination of HuggingFace's Named Entity Recognition pipeline to detect the subject and the HuggingFace's Zero Shot Classifiers to find intent from a list of possible classes. We used several apis to gather information from various sources using the results of the NLP process, we particularly focused on using the Wikipedia api to get a text body for the ai to speak. The Text to Speech was accomplished using UberDuck's API. After the processing, the content was put into an html format, loaded and displayed into unity, where an animated avatar would speak the results of the TTS

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

## What's next for Speak-2-Me
Distributed deployment, currently the platform can only exist on a single system with no way for users to view it remotely (i.e. through a browser). 

More conversational type interaction. The interaction with our avatar is very 1 turn, user asks question, bot gives answer, with limited memory or commentary tying back to previous points in the conversation. 

Better distribution of state management and processing allocation. 

---
*Copyright (c) 2022.* [AssemblyAI Hackathon](https://hackathon.assemblyai.com/)