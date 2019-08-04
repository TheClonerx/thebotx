import config

cuser = config.User(user.name)
msg = config.get_lang(cuser.lang, "hello").format(user.capser)
room.message(msg)
