# ****************************************************************************
# ***************** Common module ******************************************** 
# **************************************************************************** 

def RecordInput(record_file="/Users/cv0361/src/Hackathon/AARecording.wav"):
  import sounddevice as sd
  from scipy.io.wavfile import write

  freq = 44100    # Sampling frequency
  duration = 3    # Recording duration

  print("Start Recording.....")

  # Start recorder with the given values of duration and sample frequency
  recording = sd.rec(duration * freq, samplerate=freq, channels=1, dtype='float64')   # Check Mic input channel
    
  # Record audio for the given number of seconds
  sd.wait()
    
  print("Recorded! Recording File:", record_file)

  # This will convert the NumPy array to an audio file with the given sampling frequency
  write(record_file, freq, recording)

  return record_file

def read_audio_file(filename, chunk_size=5242880):
      with open(filename, 'rb') as _file:
          while True:
              data = _file.read(chunk_size)
              if not data:
                  break
              yield data
                         
def TranscribeAudio(record_file="/Users/cv0361/src/Hackathon/AARecording.wav"):
  import requests
  import time
  
  Token = "f50552091d9148249640201d2dc3e31f"
  
  # Upload Audio File (wav)
  headers = {'authorization': f"{Token}"}
  response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data=read_audio_file(record_file))
  resobj = response.json()
  upload_url = resobj['upload_url']
  
  # Transcribe Audio
  json = {
      "audio_url": f"{upload_url}",
      "punctuate": True,
      "format_text": False
  }
  headers = {
      "authorization": f"{Token}",
      "content-type": "application/json"
  }
  response = requests.post("https://api.assemblyai.com/v2/transcript", json=json, headers=headers)
  resobj = response.json()
  transcript_id = resobj['id']
  
  # Wait for completion and Transcription to be Available
  loop = 0
  MAX_COUNT = 30
  wait_sec = 1
  status = ""

  while (status != "completed") and (loop < MAX_COUNT):
      loop += 1
      time.sleep(wait_sec)
      
      # Get Transcript
      endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
      headers = {"authorization": f"{Token}"}
      response = requests.get(endpoint, headers=headers)
      resobj = response.json()
      status = resobj['status']
      # End 
      
      print("Waiting....", loop)
      
  if loop < MAX_COUNT:
      print("API done!")
  else:
      print("Timed out!")
  
  return resobj['text']   # Transcribed text

def SearchWiki(search_text="Dallas"):
  import wikipedia
  
  # wikipedia.set_lang("en")
  response = wikipedia.summary(search_text)

  return response

def SearchWiki_Short(search_text="Dallas", result_length=300):
  response = SearchWiki(search_text)
  response = response[0:result_length]
  position = response.rfind(" ")
  response = response[0:position]
  
  return response












# Test Function
print("\n\n***************** Testing **********************\n")

x = SearchWiki()
print("Result:", x)
x = SearchWiki_Short()
print("Result:", x)


# x = RecordInput()
# print("Result:", x)
# x = TranscribeAudio()
# print("Result:", x)

print("\n\n***************** Completed **********************\n")