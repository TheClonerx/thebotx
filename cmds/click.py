import config
import random

win = random.randint(1, 5) != 1
cuser = config.User(user.name)
lang = "en" if not cuser else cuser.lang

if win:
    msg = config.get_lang(lang, "click_win")
else:
    msg = config.get_lang(lang, "click_lose")
msg = msg.format(user.capser)
room.message(msg, True)
