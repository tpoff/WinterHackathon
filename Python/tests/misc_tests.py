import time

from Bot_Process import Bot_Process, BotLoopStep
from Text_To_Speech.Text_To_Speech import Text_To_Speech_Local_Wav_Output, Text_To_Speech_Uberduck_Wav_Output

if __name__ == "__main__":
    '''process = Bot_Process()
    process.subject = "Plane"
    process.category = "history"
    print(process.to_dict())
    process.generate_response()'''



    text_to_speech_pipeline = Text_To_Speech_Uberduck_Wav_Output()
    text = '''Hi there! I'm a bot created for the assembly aye eye Winter Hack a thon! I'm designed to answer questions about countries and other locations around the world. I'm a bit limited, but I'll try my best to tell you about different places. Ask me anything!'''
    text_to_speech_pipeline(text, "./../BotContent" + "/splash_audio.wav")
    text_to_speech_pipeline('''Allright, let me see what I can find, one moment.''', "./../BotContent" + "/lookup.wav")
    '''process = Bot_Process()
    process.start()
    print("starting bot...")
    while process.bot_loop_step == BotLoopStep.SETUP: pass

    print("starting bot loop...")
    while True:
        time.sleep(1)
        print("="*8)
        print(process.partial_message)
        print(process.last_message)
        print(process.subject)
        print(process.category)'''

    exit()