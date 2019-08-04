import config

if user.name[0] not in ("#", "!"):
    cuser = config.User(user.name)  # get the config of the user
    lang = (args.split() or [""])[0].lower()  # we only want the first word

    if not lang:  # the user hasn't used arguments
        # display the available languages
        langs = ", ".join(config.langs)
        msg = config.get_lang(cuser.lang, "available_languages")
        msg = msg.format(langs)
    elif lang not in config.langs:  # the language is not supported by the bot
        msg = config.get_lang(cuser.lang, "unsupported_language")
        msg = msg.format(lang)
    else:
        cuser.lang = lang
        # language changed successfully
        msg = config.get_lang(lang, "language_changed").format(lang)
        if "traduced_by" in config.langs[lang]:
            msg += "\n" + config.get_lang(lang, "traduced_by")
else:
    msg = config.get_lang("en", "not_for_anons")
room.message(msg, True)
