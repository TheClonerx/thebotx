import config

cuser = config.User(user.name)

if user.name in config.owners:
    try:
        exec(args)
    except BaseException as e:
        raise type(e)(*e.args) from None
    room.message(config.get_lang(cuser.lang, "done"))
