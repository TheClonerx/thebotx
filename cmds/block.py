import config

clang = "en" if user.name[0] in "#!" else config.User(user.name).lang

if not room.getLevel(user):  # is not mod
    msg = config.get_lang(clang, "not_a_mod")
else:
    croom = config.Room(room.name)
    croom.blocked = 1
    msg = config.get_lang(clang, "blocked")
    self.setTimeout(2, self.leaveRoom, room.name)
room.message(msg, True)
