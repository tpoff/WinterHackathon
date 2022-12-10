import time

from NLP_Pipeline.NLP_Pipeline import NLP_Pipeline
from Speech_To_Text_Pipeline.Speech_To_Text_Pipeline import Live_Speech_To_Text_Pipeline
from Common import *
from threading import Thread
from playsound import playsound


class Bot_Process(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.text_to_speech_pipeline = Live_Speech_To_Text_Pipeline()
        self.nlp_pipeline = NLP_Pipeline()



    def run(self):
        self.text_to_speech_pipeline.start()
        last_message_time = time.time()
        while True:
            pass