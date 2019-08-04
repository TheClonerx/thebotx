import config

clang = "en" if user.name[0] in "#!" else config.User(user.name).lang

if not args.strip():
    msg = config.get_lang(clang, "users")
    msg = msg.format(
        room.name,
        ", ".join(sorted(set(x.capser for x in room.userlist), key=lambda x: x.lower()))
    )
else:
    rname = args.split()[0].lower()
    if rname not in self._rooms:
        msg = config.get_lang(clang, "not_in_room")
        msg = msg.format(rname)
    else:
        msg = config.get_lang(clang, "users")
        msg = msg.format(
            rname,
            ", ".join(
                sorted(set(x.capser for x in self._rooms[rname].userlist), key=lambda x: x.lower())
            )
        )
room.message(msg, True)
