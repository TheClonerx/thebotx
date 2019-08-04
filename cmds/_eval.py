import config

if user.name in config.owners:
    try:
        room.message(repr(eval(args)))
    except BaseException as e:
        raise type(e)(*e.args) from None
