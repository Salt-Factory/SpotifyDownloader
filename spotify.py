import sys
import spotipy
import spotipy.util as util
import os
import urllib
import re
import sys
import unidecode
from mutagen.oggvorbis import OggVorbis
import glob

##############################################################################
"""
Many thanks to Grant Curell over at
https://www.codeproject.com/articles/873060/python-search-youtube-for-video
All I had to do was switch it over to Python2
just had to switch to import urllib (urllib is split in three for Python3),
and add the "utf8" in the .decode()
"""
def getUrl(query):
    query = unidecode.unidecode(query)
    query_string = urllib.urlencode({"search_query" : query})
    html_content = urllib.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall((r'href=\"\/watch\?v=(.{11})'), html_content.read().decode("utf8"))
    return "http://www.youtube.com/watch?v=" + search_results[0],search_results[0]


#Downloads the video located at the URL & converts it into .mp3 using youtube-dl
#converting uses ffmpeg
def download(url):
    os.system('youtube-dl -x --audio-format "vorbis" '+  url)



#looks for the full filename based on the URI,returns an array of hits
#as URI is unique, only one hit can be found so the first value will be used
def findFileName(URI):
    files = glob.glob("*"+URI+".ogg") #build-in function to find files

    filename = files[0]
    return filename

#add the tags (taken from Spotify) to the audiofiles
def addTags(filename,track):
    print track['name']

    audio = OggVorbis(filename)
    audio["title"] = track['name']
    audio["artist"] = track['artists'][0]['name']
    audio["album"] = track['album']['name']
    audio.save()
    print(audio.pprint())
    os.rename(filename,track['name']+".ogg")
    print track['album']['images'][0]['url']

##############################################################################
def main():
    scope = 'user-library-read' #set scope for Spotify AUTH
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print "Usage: %s username" % (sys.argv[0],)
        sys.exit()

    token = util.prompt_for_user_token(username,scope,client_id='',client_secret='',redirect_uri='http://localhost/')

    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_saved_tracks()
        for item in results['items']:
            track = item['track']
            print item['release_date']
            print track['album']['release_date']
            url,URI = getUrl(track['name']+ " "+ track['artists'][0]['name'])
            download(url)
            filename = findFileName(URI)
            addTags(filename,track)

            break

    else:
        print "Can't get token for", username


main()
