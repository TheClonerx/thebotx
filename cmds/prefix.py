import config
import html

if user.name[0] not in ("#", "!"):
    cuser = config.User(user.name)
    if not args.strip():
        msg = config.get_lang(cuser.lang, "current_prefix")
        msg = msg.format(html.escape(cuser.prefix))
    else:
        new_prefix = args.split()[0]
        if len(new_prefix) > 5:
            msg = config.get_lang(cuser.lang, "prefix_too_long")
        elif new_prefix[0] == "_":
            msg = config.get_lang(cuser.lang, "invalid_prefix")
        else:
            cuser.prefix = new_prefix
            msg = config.get_lang(cuser.lang, "new_prefix")
        msg = msg.format(html.escape(new_prefix))
else:
    msg = config.get_lang("en", "not_for_anons")
room.message(msg, True)
