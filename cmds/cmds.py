import config

clang = "en" if user.name[0] in "#!" else config.User(user.name).lang
if user.name in config.owners:
    cmds = config.cmds.keys()
else:
    cmds = [x for x in config.cmds.keys() if x[0] != "_"]
msg = config.get_lang(clang, "available_commands")
msg = msg.format(", ".join(sorted(cmds)))
room.message(msg, True)
