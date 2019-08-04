import os
import sys
import time

start_time = time.time()
sys.path.append(os.path.join(os.getcwd(), "libs"))

import bot
import config


def main():
    config.connect_db()
    config.load_all()
    my_bot = bot.Bot(
        config.auth["name"], config.auth["password"], config.auth["pm"]
    )
    my_bot.start_time = start_time
    for room in config.Room.room_names:
        room = config.Room(room)
        if not room.blocked:
            my_bot.joinRoom(room.name)
    try:
        my_bot.main()
    finally:
        config.save_all()
        config.database.commit()
        config.disconnect_db()

if __name__ == '__main__':
    main()
