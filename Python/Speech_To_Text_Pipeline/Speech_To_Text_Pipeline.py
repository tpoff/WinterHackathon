# needs a clean exit! currently leaves threads hanging

import pyaudio
import websockets
import asyncio
import base64
import json
import time
from threading import Thread

auth_key = "b9be974194ad478e99a45c3f8b2b5824"
FRAMES_PER_BUFFER = 3200
FRAMES_PER_BUFFER = 1600
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

class Live_Speech_To_Text_Pipeline(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.reading_message = False
        self.last_message = ""
        self.partial_message = ""
        self.last_message_time = time.time()
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER)

    def run(self):
        async def send_receive():
            print(f'Connecting websocket to url ${URL}')
            async with websockets.connect(
                    URL,
                    extra_headers=(("Authorization", auth_key),),
                    ping_interval=5,
                    ping_timeout=20
            ) as _ws:
                await asyncio.sleep(0.1)
                print("Receiving SessionBegins ...")
                session_begins = await _ws.recv()
                print(session_begins)
                print("Sending messages ...")
                start_time = time.time()

                async def send():
                    while True:
                        try:
                            data = self.stream.read(FRAMES_PER_BUFFER)
                            data = base64.b64encode(data).decode("utf-8")
                            json_data = json.dumps({"audio_data": str(data)})
                            await _ws.send(json_data)
                        except websockets.exceptions.ConnectionClosedError as e:
                            print(e)
                            assert e.code == 4008
                            break
                        except Exception as e:
                            assert False, "Not a websocket 4008 error"
                        await asyncio.sleep(0.01)

                    return True

                async def receive():
                    while True:
                        try:

                            result_str = await _ws.recv()
                            # keys in return json: message_type, session_id,
                            # audio_start, audio_end, confidence, text, words, created (timestamp of original request)
                            '''
                            so the api usually returns 2 calls a second. When the end of a statement is reached it resets
                            the message
                            
                            ok, so when the api resets a message due to silence, it returns a puncuation corrected version
                            of the last message in the last call.
                            However there will be a series of 2-3 calls that contain the same info before the api pulls
                            the plug.
                            
                            2 if the messages are > .5 seconds apart, 3 if the first 2 are less than .5 seconds.
                            That gives us some wiggle room to end the process early rather than wait for the api to reset
                            the return string, 
                            
                            2 messages that contain the same and > .5 seconds = cut message 
                            3 messages = cut message,
                            
                            no need to wait for that final message to return
                            
                            so basically it appears taht the api hears .5 seconds of silence it resets the message
                            based on the changing contents (or lack thereof) and when messages come in we can
                            predict the end of a statement without the api telling us. 
                            '''
                            result = json.loads(result_str)

                            # checking if the api has reset the text indicating the end of a statement,
                            read_status = result['text'] != ''
                            if not read_status and self.reading_message == True:
                                self.last_message = self.partial_message
                                self.last_message_time = time.time()
                            self.reading_message = read_status
                            self.partial_message = result['text']


                        except websockets.exceptions.ConnectionClosedError as e:
                            print(e)
                            assert e.code == 4008
                            break
                        except Exception as e:
                            assert False, "Not a websocket 4008 error"

                send_result, receive_result = await asyncio.gather(send(), receive())

        asyncio.run(send_receive())



if __name__ == "__main__":
    pipeline = Live_Speech_To_Text_Pipeline()
    pipeline.start()
    while True:
        time.sleep(1)
        print(pipeline.reading_message)
        print(pipeline.last_message)
        print(pipeline.last_message_time)

    sys.exit()