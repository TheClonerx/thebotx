import config
import urllib.request
import utils
import datetime
import time
import re
import ch
import html
import concurrent.futures
import xml.etree.ElementTree
import bs4


def fetch(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return response.read()


clang = "en" if user.name[0] in "#!" else config.User(user.name).lang

if not args.strip() and user.name[0] in "!#":
    msg = config.get_lang(clang, "not_for_anons")
else:
    if not args.strip():
        name = user.name
    else:
        name = args.split()[0].lower()

    frmt = name[0], name[1] if len(name) > 1 else name[0], name
    url1 = "http://ust.chatango.com/profileimg/{}/{}/{}/".format(*frmt)
    url2 = "http://fp.chatango.com/profileimg/{}/{}/{}/" .format(*frmt)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future1 = executor.submit(fetch, url1 + "mod1.xml", 10)
        future2 = executor.submit(fetch, url1 + "mod2.xml", 10)
        mod1 = future1.result()
        mod2 = future2.result()

    if mod1 == utils.DEFAULT_IMG:
        mod1 = None
    else:
        mod1 = xml.etree.ElementTree.XML(mod1)
        if mod1.find("body") is not None:
            mini_profile = mod1.find("body").text
            mini_profile = urllib.request.unquote(mini_profile).strip()
            mini_profile = re.sub(
                r'<style.*?>.*?</style>', "", mini_profile, 0, re.I | re.M
            )
            mini_profile = re.sub(
                r'<script.*?>.*?</script>', "", mini_profile, 0, re.I | re.M
            )
            mini_profile = re.sub(
                r'<br/?>', "\n", mini_profile, 0, re.I | re.M
            )
            mini_profile = re.sub(
                r'</br>', "", mini_profile, 0, re.I | re.M
            )
            mini_profile = bs4.BeautifulSoup(mini_profile, "html.parser")
            mini_profile = " ".join(mini_profile.text.split())
        else:
            mini_profile = ""
        gender = mod1.find("s").text if mod1.find("s") is not None else None
        if mod1.find("b") is not None:
            age = mod1.find("b").text
            age = datetime.datetime.strptime(age, "%Y-%m-%d")
            now = datetime.datetime.now()
            age = now.year - age.year
        else:
            age = None
        location = mod1.find("l").text if mod1.find("l") is not None else None
        if mini_profile:
            if len(mini_profile) > 250:
                mini_profile = mini_profile[:250] + "..."
            mini_profile = config.get_lang(clang, "who_mprofile").format(
                html.escape(mini_profile)
            )
        if gender:
            gender = config.get_lang(clang, "gender_" + gender.lower())
            gender = config.get_lang(clang, "who_gender").format(gender)
        if age:
            age = config.get_lang(clang, "who_age").format(age)
        if location:
            location = config.get_lang(clang, "who_location").format(location)

    if mod2 == utils.DEFAULT_IMG:
        mod2 = None
    else:
        mod2 = xml.etree.ElementTree.XML(mod2)
        if mod2.find("body") is not None:
            full_profile = mod2.find("body").text
            full_profile = urllib.request.unquote(full_profile).strip()
            full_profile = re.sub(
                r'<style.*?>.*?</style>', "", full_profile, 0, re.I | re.M
            )
            full_profile = re.sub(
                r'<script.*?>.*?</script>', "", full_profile, 0, re.I | re.M
            )
            full_profile = re.sub(
                r'<br/?>', "\n", full_profile, 0, re.I | re.M
            )
            full_profile = re.sub(
                r'</br>', "", full_profile, 0, re.I | re.M
            )
            full_profile = bs4.BeautifulSoup(full_profile, "html.parser")
            full_profile = " ".join(full_profile.text.split())
            if len(full_profile) > 250:
                full_profile = full_profile[:250] + "..."
        else:
            full_profile = ""
        if full_profile:
            full_profile = config.get_lang(clang, "who_fprofile").format(
                html.escape(full_profile)
            )

    picture = url2 + "full.jpg"
    with urllib.request.urlopen(picture) as res:
        pic = res.read(len(utils.DEFAULT_IMG))
        res.close()

    if pic == utils.DEFAULT_IMG:
        picture = None
    else:
        picture = config.get_lang(clang, "who_image").format(picture)

    if not mod1 and not mod2 and not picture:
        msg = config.get_lang(clang, "cant_get_user").format(name)
    else:
        msg = config.get_lang(clang, "who_name").format(ch.User(name).capser)
        if mod1 and mini_profile:
            msg += "\n &nbsp; &nbsp;" + mini_profile
        if mod2 and full_profile:
            msg += "\n &nbsp; &nbsp;" + full_profile
        if mod1 and gender:
            msg += "\n &nbsp; &nbsp;" + gender
        if mod1 and age:
            msg += "\n &nbsp; &nbsp;" + age
        if mod1 and location:
            msg += "\n &nbsp; &nbsp;" + location
        if mod1 and picture:
            msg += "\n &nbsp; &nbsp;" + picture
room.message(msg, True)
