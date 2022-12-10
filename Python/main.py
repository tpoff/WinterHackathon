import time

from Bot_Process.Bot_Process import Bot_Process

if __name__ == "__main__":

    process = Bot_Process()
    process.run()
    while True:
        time.sleep(1)
        print(process.last_message)
        print(process.subject)
        print(process.category)

    exit()