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
    SUCCESS = 0
    FAILURE = 1

class Bot_Process(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.bot_loop_step = BotLoopStep.SETUP
        self.speech_to_text_pipeline = Live_Speech_To_Text_Pipeline()
        self.nlp_pipeline = NLP_Pipeline()
        self.text_to_speech_pipeline = Text_To_Speech_Local_Wav_Output()

        self.last_message_time = self.speech_to_text_pipeline.last_message_time

        self.last_round_status = LastRoundStatus.SUCCESS

        self.subject = ""
        self.category = ""

    @property
    def last_message(self):
        return self.speech_to_text_pipeline.last_message

    def run(self):
        self.speech_to_text_pipeline.start()

        while not self.speech_to_text_pipeline.ready:
            time.sleep(.25)
        while True:
            self.bot_round()

    def bot_round(self):
        print("in standby...")
        self.bot_loop_step = BotLoopStep.STANDBY

        while not self.speech_to_text_pipeline.reading_message and\
                self.last_message_time == self.speech_to_text_pipeline.last_message_time:
            time.sleep(.1)

        print("listening to message...")
        self.bot_loop_step = BotLoopStep.READING_MESSAGE

        while self.last_message_time == self.speech_to_text_pipeline.last_message_time:
            time.sleep(.1)

        self.last_message_time = self.speech_to_text_pipeline.last_message_time


        print("processing nlp...")
        self.bot_loop_step = BotLoopStep.PROCESSING_NLP
        self.subject,  self.category = self.nlp_pipeline(self.last_message)

        print("constructing responses...")
        self.bot_loop_step = BotLoopStep.DATA_LOOKUP
        # TODO
        time.sleep(1)

        print("that's all folks, ")
        self.bot_loop_step = BotLoopStep.STANDBY






