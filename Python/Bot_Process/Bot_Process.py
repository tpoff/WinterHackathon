import time

from NLP_Pipeline.NLP_Pipeline import NLP_Pipeline
from Speech_To_Text_Pipeline.Speech_To_Text_Pipeline import Live_Speech_To_Text_Pipeline
from Text_To_Speech.Text_To_Speech import Text_To_Speech_Local_Wav_Output
from Common import *
from threading import Thread
from playsound import playsound
from enum import Enum

class BotLoopStep(Enum):
    SETUP = 0
    STANDBY = 1
    READING_MESSAGE = 2
    PROCESSING_NLP = 3
    DATA_LOOKUP = 4

class LastRoundStatus(Enum):
    NOT_RUN=0
    SUCCESS = 1
    NO_SUBJECT = 2

class Bot_Process(Thread):
    def __init__(self, response_output_directory="./"):
        Thread.__init__(self)
        self.bot_loop_step = BotLoopStep.SETUP
        self.speech_to_text_pipeline = Live_Speech_To_Text_Pipeline()
        self.nlp_pipeline = NLP_Pipeline()
        self.text_to_speech_pipeline = Text_To_Speech_Local_Wav_Output()

        self.last_message_time = self.speech_to_text_pipeline.last_message_time

        self.last_round_status = LastRoundStatus.NOT_RUN

        self.subject = ""
        self.category = ""
        self.last_response_ready = time.time()
        self.response_output_directory = response_output_directory

    def to_dict(self):
        return {
            "LastRoundStatus": str(self.last_round_status).split(".")[-1],
            "LastMessageTime": self.last_message_time,
            "LastMessage": self.last_message,
            "PartialMessage": self.partial_message,
            "BotLoopStep": str(self.bot_loop_step).split(".")[-1],
            "Subject": self.subject,
            "Category": self.category,
        }

    @property
    def last_message(self):
        return self.speech_to_text_pipeline.last_message
    @property
    def partial_message(self):
        return self.speech_to_text_pipeline.partial_message

    def run(self):
        self.speech_to_text_pipeline.start()

        while not self.speech_to_text_pipeline.ready:
            time.sleep(.25)
        while True:
            self.bot_round()


    def generate_response(self):
        # TODO
        print(self.subject, self.category)
        #wiki_text = SearchWiki_WithContext(search_text=self.subject, context=self.category)
        #prompt = self.subject + " " + self.category
        #youtube_content = SearchYoutube(prompt)
        #flickr_content = SearchFlickr(prompt)
        #twitter_content = SearchTwitter(prompt)
        self.text_to_speech_pipeline("and here we go again", "./temp.wav")

    def bot_round(self, verbose=False):
        if verbose: print("in standby...")
        self.bot_loop_step = BotLoopStep.STANDBY

        while not self.speech_to_text_pipeline.reading_message and\
                self.last_message_time == self.speech_to_text_pipeline.last_message_time:
            time.sleep(.1)

        if verbose: print("listening to message...")
        self.bot_loop_step = BotLoopStep.READING_MESSAGE

        while self.last_message_time == self.speech_to_text_pipeline.last_message_time:
            time.sleep(.1)

        self.last_message_time = self.speech_to_text_pipeline.last_message_time


        if verbose: print("processing nlp...")
        self.bot_loop_step = BotLoopStep.PROCESSING_NLP
        self.subject,  self.category = self.nlp_pipeline(self.last_message)

        if verbose: print("constructing responses...")
        self.bot_loop_step = BotLoopStep.DATA_LOOKUP
        self.generate_response()
        self.last_response_ready = time.time()


        if verbose: print("end of round, ")
        self.bot_loop_step = BotLoopStep.STANDBY






