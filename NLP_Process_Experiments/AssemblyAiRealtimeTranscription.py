# reference documentation: https://www.assemblyai.com/docs/walkthroughs#realtime-streaming-transcription
# https://www.assemblyai.com/blog/real-time-speech-recognition-with-python/ python reference
import pyaudio
import websockets
import asyncio
import base64
import json
import time

auth_key = "b9be974194ad478e99a45c3f8b2b5824"
FRAMES_PER_BUFFER = 3200
FRAMES_PER_BUFFER = 1600
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER)
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"


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
                    data = stream.read(FRAMES_PER_BUFFER)
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
                    result = json.loads(result_str)
                    current = time.time()
                    if result['text'] == '':
                        start_time = current
                    print(result['text'])
                    print(current - start_time)
                    #print(result['audio_start'], result['audio_end'], result['audio_end']-result['audio_start'])

                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"

        send_result, receive_result = await asyncio.gather(send(), receive())





asyncio.run(send_receive())

print("and so we begin")
while True:
    time.sleep(5)
    print("ping")