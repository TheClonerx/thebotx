import config
import re
from utils import DotDict
clang = "en" if user.name[0] in "#!" else config.User(user.name).lang

room_re = re.compile(r'^\s*(https?:\/\/)?([a-z0-9-]+)(\.chatango\.com)?', re.I)

if not args.strip():
    msg = config.get_lang(clang, "missing_argument")
    arg = config.get_lang(clang, "argument_room")
    msg = msg.format(arg)
elif not room_re.match(args):
    msg = config.get_lang(clang, "invalid_room").format(args)
else:
    aroom = room_re.match(args).groups()[1].lower()
    if aroom in config.Room.room_names:
        msg = config.get_lang(clang, "already_joined")
        msg = msg.format(aroom)
    else:
        cursor = config.database.cursor()
        cursor.execute(
            "insert into rooms (name) values (%s)",
            (aroom,)
        )
        config.database.commit()
        cursor.close()
        self.joinRoom(aroom)
        msg = config.get_lang(clang, "joining").format(aroom)
room.message(msg, True)
