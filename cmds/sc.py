import config
import urllib.request
import json
import html

clang = "en" if user.name[0] in "#!" else config.User(user.name).lang

url = (
    "http://api.soundcloud.com/tracks/"
    "?client_id=SOUNDCLOUD_CLIENT_ID&q="
)

if not args:
    msg = config.get_lang(clang, "missing_argument")
    arg = config.get_lang(clang, "argument_query")
    msg = msg.format(arg)
else:
    query = urllib.request.quote(args)
    response = urllib.request.urlopen(url + query)
    data = json.loads(response.read().decode())
    if not data:
        msg = config.get_lang(clang, "cant_found_video")
        msg = msg.format("SoundCloud", html.escape(args))
    else:
        track = data[0]
        title = track["title"]
        user = track["user"]["username"]
        url = track["permalink_url"]
        msg = config.get_lang(clang, "found_video")
        title = html.escape(title)
        user = html.escape(user)
        msg = msg.format(title, user, url)
room.message(msg, True)
