import urllib.request
import re
import json
import sys

def parse_spotify(url):
    embed_url = url.replace("spotify.com/", "spotify.com/embed/").split("?")[0]
    req = urllib.request.Request(embed_url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')

    json_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', html)
    data = json.loads(json_data.group(1))
    entity = data['props']['pageProps']['state']['data']['entity']
    
    if entity['type'] in ['playlist', 'album']:
        tracks = entity['trackList']
        for t in tracks:
             print(f"{t['title']} - {t['subtitle']}")
    elif entity['type'] == 'track':
        print(f"TRACK: {entity.get('name')} - Keys: {entity.keys()}")
    else:
        print(entity.keys())

parse_spotify('https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT')
parse_spotify('https://open.spotify.com/album/4aawyAB9vmqN3uQ7FjRGTy')
