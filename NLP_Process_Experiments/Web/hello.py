from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, There!'

@app.route('/api/test')
def index():
    return jsonify([{'name': 'Dallas',
                        'email': 'Dallas@outlook.com'
                    },
                    {'name': 'jack',
                        'email': 'jack@outlook.com'
                    }]
                    )

@app.route('/api/youtube')
def GetYoutube():
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
            q="Dallas Texas Interesting Fact",
            videoDuration='short',
            videoDefinition='high',
            maxResults=10
        )

    # Request execution
    response = request.execute()

    # Build HTML Content List
    strhtml = """
    <table width='500px' cellpadding='5' border='1'>
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

@app.route('/api/flickr')
def Getflickr():
    from flickrapi import FlickrAPI

    FLICKR_PUBLIC = '70871ff16d3a400b1c4675bd423abd13'
    FLICKR_SECRET = 'cee2f7226982315d'

    flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
    extras = 'url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'
    response = flickr.photos.search(text='Dallas Texas landscape', sort="relevance", per_page=30, extras=extras)

    # Build HTML Content
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
        
        strhtml += f"<a target='_blank' href='{Large}'><img src='{Thumbnail}'></a>" 
        
    strhtml += "</td></tr></table>"  

    return strhtml


