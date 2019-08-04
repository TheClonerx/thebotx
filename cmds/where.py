import config
import ch

clang = "en" if user.name[0] in "#!" else config.User(user.name).lang

if not args.strip():
    msg = config.get_lang(clang, "missing_argument")
    msg = msg.format(config.get_lang(clang, "argument_user"))
else:
    name = args.split()[0].lower()
    capser = ch.User(name).capser
    rooms = list(sorted(x.name for x in self.rooms if name in x.usernames))
    if not rooms:
        msg = config.get_lang(clang, "user_not_found")
        msg = msg.format(capser)
    else:
        msg = config.get_lang(clang, "user_found")
        msg = msg.format(capser, ", ".join(rooms))
room.message(msg, True)
