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

def SearchYoutube(search_text="Dallas Interesting Fact", result_count=10):
  import googleapiclient.discovery
  
  # API information
  api_service_name = "youtube"
  api_version = "v3"
  DEVELOPER_KEY = 'AIzaSyDckal4boKo3Bq4ejBpCtTMvIHH56TGPTE'
  
  # API client
  youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)

  # Request body
  request = youtube.search().list(
          part="snippet",
          type='video',
          order="relevance",
          q=search_text,
          videoDuration='short',
          videoDefinition='high',
          maxResults=result_count
      )

  # Request execution
  return request.execute()

def SearchYoutube_GetHTML(search_text="Dallas Interesting Fact", result_count=10):
  response = SearchYoutube(search_text, result_count)
  
  # Build HTML Content List
  strhtml = """
  <table width='500px' cellpadding='1'>
  """

  for item in response['items']:
      VideoId = item['id']['videoId']
      Title = item['snippet']['title']
      Description = item['snippet']['description']
      Thumbnail = item['snippet']['thumbnails']['default']['url']
      
      strhtml += f"""
      <tr>
        <td rowspan=2 width='120px'><a target='_blank' href='http://www.youtube.com/watch?v={VideoId}'><img src='{Thumbnail}'></a></td>
        <td align='left'><a target='_blank' href='http://www.youtube.com/watch?v={VideoId}'>{Title}</a></td>
      </tr>
      <tr>
        <td align='left'>{Description}</td>
      </tr>
      """ 
      
  strhtml += "</table>"    
  
  return strhtml

def SearchFlickr(search_text="Dallas Texas landscape", result_count=30):
  from flickrapi import FlickrAPI
  
  FLICKR_PUBLIC = '70871ff16d3a400b1c4675bd423abd13'
  FLICKR_SECRET = 'cee2f7226982315d'

  flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
  extras = 'url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'
  
  return flickr.photos.search(text=search_text, sort="relevance", per_page=result_count, extras=extras)
    
def SearchFlickr_GetHTML(search_text="Dallas Texas landscape", result_count=30):
  response = SearchFlickr(search_text, result_count)
  
  # Build HTML Content List
  strhtml = """
  <table width='540px' cellpadding='1'>
  <tr><td>
  """

  for item in response['photos']['photo']:
      Thumbnail = item['url_t']
      
      try:
          Large = item['url_l']
      except:
          try:
              Large = item['url_o']
          except:
              pass
      
      strhtml += f"<a target='_blank' href='{Large}'><img src='{Thumbnail}'></a> " 
      
  strhtml += "</td></tr></table>"  

  return strhtml

def Twitter_bearer_oauth(r):
    bearer_token = "AAAAAAAAAAAAAAAAAAAAALXOkAEAAAAAJcMmA%2BymvGkz8qZdBybQIFXVgAQ%3DB7lXrSS2OzjBiVuzAGsI8OIZhDt80TnD8KXNdh6xKAxI0IJsh1"
    
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    
    return r

def SearchTwitter(search_text="Dallas Interesting", result_count=15):
  import requests
  import json
  
  # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
  # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
  query_params = {'query': search_text,
                  'tweet.fields': 'author_id',
                  'sort_order': 'relevancy',
                  'max_results': result_count
                }

  response = requests.get("https://api.twitter.com/2/tweets/search/recent", auth=Twitter_bearer_oauth, params=query_params)
  
  if response.status_code != 200:
      raise Exception(response.status_code, response.text)
  
  return response.json()




# Test Functions
print("\n\n***************** Testing **********************\n")

x = SearchTwitter()
print("Result:", x)



# x = RecordInput()
# print("Result:", x)
# x = TranscribeAudio()
# print("Result:", x)

# x = SearchWiki()
# print("Result:", x)
# x = SearchWiki_Short()
# print("Result:", x)

# x = SearchYoutube()
# print("Result:", x)
# x = SearchYoutube_GetHTML(search_text="Tokyo Interesting Fact", result_count=50)
# print("Result:", x)

# x = SearchFlickr()
# print("Result:", x)
# x = SearchFlickr_GetHTML(search_text="Dallas Texas landscape", result_count=50)
# print("Result:", x)

print("\n\n***************** Completed **********************\n")