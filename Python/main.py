import time

from Bot_Process.Bot_Process import Bot_Process, BotLoopStep

if __name__ == "__main__":

    process = Bot_Process()
    print(process.to_dict())
    '''process.start()
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