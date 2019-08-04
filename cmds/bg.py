# -*- coding: utf-8 -*-
import urllib.request
import concurrent.futures
import xml.etree.ElementTree
import ch
import config
import utils


def fetch(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return response.read()


args = args.split()
clang = "en" if user.name[0] in "#!" else config.User(user.name).lang
if not args and user.name[0] in "#!":
    msg = config.get_lang(clang, "not_for_anons")
else:
    if not args:
        name = user.name
    else:
        name = args[0].lower()
    url = "http://ust.chatango.com/profileimg/{}/{}/{}/".format(
        name[0], name[1] if len(name) > 1 else name[0], name
    )

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future1 = executor.submit(fetch, url + "mod1.xml", 10)
        future2 = executor.submit(fetch, url + "msgbg.xml", 10)
        mod1 = future1.result()
        msgbg = future2.result()

    if mod1 == utils.DEFAULT_IMG:
        mod1 = None
    else:
        mod1 = xml.etree.ElementTree.XML(mod1)
        bgtime = int(mod1.find("d").text)
    if msgbg == utils.DEFAULT_IMG:
        msgbg = None
        col = '<f x{0}FFF="{1}">██████<f x{0}{2}="{1}">'.format(
            str(self.user.fontSize).zfill(2), self.user.fontFace,
            self.user.fontColor
        )
        rgba = "rgba(255, 255, 255, 1)"
    else:
        msgbg = xml.etree.ElementTree.XML(msgbg)
        a = float(msgbg.get("bgalp")) / 100
        rgb = msgbg.get("bgc")
        if len(rgb) == 3:
            r, g, b = (int(x, 16) * 15 for x in rgb)
        else:
            r, g, b = (
                int(rgb[i * 2:i * 2 + 2], 16) for i in range(int(len(rgb) / 2))
            )
        base = [255, 255, 255]
        mix = [0, 0, 0]
        mix[0] = round((1 - a) * 255 + a * r)
        mix[1] = round((1 - a) * 255 + a * g)
        mix[2] = round((1 - a) * 255 + a * b)
        col = "{}{}{}".format(*(hex(x)[2:].zfill(2) for x in mix))
        col = '<f x{0}{1}="{2}">██████<f x{0}{3}="{2}">'.format(
            str(self.user.fontSize).zfill(2), col, self.user.fontFace,
            self.user.fontColor
        )
        rgba = "rgba({}, {}, {}, {})".format(r, g, b, a)
    if not mod1 and not msgbg:
        msg = config.get_lang(clang, "cant_get_user").format(name)
    else:
        msg = config.get_lang(clang, "background")
        if not bgtime:
            bgtime = config.get_lang(clang, "time_expired").format("?")
        else:
            delta = utils.delta_time(bgtime)
            bgtime = utils.str_delta(clang, delta)
            if delta.past:
                bgtime = config.get_lang(clang, "time_expired").format(bgtime)
        msg = msg.format(
            ch.User(name).capser, col, rgba, bgtime, url + "msgbg.jpg"
        )
room.message(msg, html=True)
