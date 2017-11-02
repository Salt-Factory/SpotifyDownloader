//The original youtube search by Grant Curell over at
//https://www.codeproject.com/articles/873060/python-search-youtube-for-video

import urllib.request
import urllib.parse
import re
import sys


query = ""
i = 1;
try:
    while 1:
        query +=sys.argv[i]+" "
        i+=1
except:
    print(query)

query_string = urllib.parse.urlencode({"search_query" : query})
print(query_string)
html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
print("http://www.youtube.com/watch?v=" + search_results[0])
