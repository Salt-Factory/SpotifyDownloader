import sys
import spotipy
import spotipy.util as util
import os
import urllib
import re
import sys


//Many thanks to Grant Curell over at https://www.codeproject.com/articles/873060/python-search-youtube-for-video
//All I had to do was switch it over to Python2
//just had to switch to import urllib (urllib is split in three for Python3), and add the "utf8" in the .decode()
def getUrl(query):
    query_string = urllib.urlencode({"search_query" : query})
    print query_string
    html_content = urllib.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall((r'href=\"\/watch\?v=(.{11})'), html_content.read().decode("utf8"))
    print "http://www.youtube.com/watch?v=" + search_results[0]




scope = 'user-library-read'
if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username,scope,client_id='479fdd89bbf24dba9ce84355fc159ba7',client_secret='7538d37645184848868496703eed4b18',redirect_uri='http://localhost/')

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        getUrl(track['name']+ " "+ track['artists'][0]['name'])
        break

else:
    print "Can't get token for", username
