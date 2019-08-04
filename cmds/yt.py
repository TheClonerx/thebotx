
import config
import urllib.request
import json
import sys
import html
clang = "en" if user.name[0] in "#!" else config.User(user.name).lang
url = (
    "https://www.googleapis.com/youtube/v3/search?q={}&part=snippet"
    "&maxResults=10&key=YOUTUBE_API_ID"
)


if not args.strip():
    msg = config.get_lang(clang, "missing_argument")
    msg = msg.format(config.get_lang(clang, "argument_query"))
else:
    query = urllib.request.quote(args)
    url = url.format(query)
    res = urllib.request.urlopen(url)
    data = json.loads(res.read().decode())
    if not data["items"]:
        msg = config.get_lang(clang, "cant_found_video")
        msg = msg.format("YouTube", html.escape(args))
    else:
        item = data["items"][0]
        if item["id"]["kind"] == "youtube#video":
            video_id = item["id"]["videoId"]
            video_title = item["snippet"]["title"]
            channel_name = item["snippet"]["channelTitle"]
            video_url = "https://youtu.be/" + video_id
            video_title = html.escape(video_title)
            channel_name = html.escape(channel_name)

            msg = config.get_lang(clang, "found_video")
            msg = msg.format(video_title, channel_name, video_url)
        elif item["id"]["kind"] == "youtube#playlist":
            playlist_id = item["id"]["playlistId"]
            playlist_title = item["snippet"]["title"]
            playlist_url = (
                "https://www.youtube.com/playlist?list="
            ) + playlist_id
            channel_name = item["snippet"]["channelTitle"]

            playlist_title = html.escape(playlist_title)
            channel_name = html.escape(channel_name)

            msg = config.get_lang(clang, "found_video")
            msg = msg.format(playlist_title, channel_name, playlist_url)
        elif item["id"]["kind"] == "youtube#channel":
            channel_id = item["id"]["channelId"]
            channel_title = item["snippet"]["title"]
            channel_thumb = item["snippet"]["thumbnails"]["default"]["url"]
            channel_url = (
                "https://www.youtube.com/channel/"
            ) + channel_id
            msg = config.get_lang(clang, "found_channel")
            msg = msg.format(channel_title, channel_thumb, channel_url)
        else:
            msg = "Unkown type " + item["id"]["kind"]
room.message(msg, html=True)
