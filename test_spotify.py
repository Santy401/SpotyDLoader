import urllib.request
import re
import json
url = 'https://open.spotify.com/embed/playlist/44amniurVKnB40krJwobII'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')

# Grab the Next.js __NEXT_DATA__ JSON from the embed page
json_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', html)
if json_data:
    data = json.loads(json_data.group(1))
    tracks = data['props']['pageProps']['state']['data']['entity']['trackList']
    for t in tracks:
        print(t['title'], t['subtitle'])
