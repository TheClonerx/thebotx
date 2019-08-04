import ch
import config
import sys
import os
from utils import event

import html
import traceback
import time
import random


class Bot(ch.RoomManager):
    @event
    def onInit(self):
        self.enableBg()
        self.setFontColor("F00")
        self.setFontSize(14)
        self.setFontFace(7)
        self.setNameColor("C00")

    @event
    def onPMMessage(self, pm, user, body):
        pass

    @event
    def onDisconnect(self, room):
        if room.name in config.Room.room_names and not config.Room(room.name).blocked:
            self.joinRoom(room.name)

    @event
    def onConnect(self, room):
        croom = config.Room(room.name)
        if croom.blocked:
            self.leaveRoom(room.name)
        room.channels = croom.channels

    @event
    def onConnectFail(self, room):
        if room.name in config.Room.room_names:
            config.Room.del_room(room.name)

    @event
    def onMessage(self, room, user, message):
        if user == self.user:
            return
        if not message.body.strip():
            return

        msgdata = message.body.strip().split(" ", 1)

        PREFIX = config.User(user.name).prefix

        if len(msgdata) == 2:
            cmd, args = msgdata
        else:
            cmd, args = msgdata[0], ""

        if cmd == PREFIX:
            msgdata = args.split(" ", 1)
            if len(msgdata) == 2:
                cmd, args = msgdata
            else:
                cmd, args = msgdata[0], ""
        elif (cmd.lower() == "@" +
                self.user.name.replace("#", "").replace("!", "")):
            msgdata = args.split(" ", 1)
            if len(msgdata) == 2:
                cmd, args = msgdata
            else:
                cmd, args = msgdata[0], ""

        elif cmd[:len(PREFIX)] == PREFIX:
            cmd = cmd[len(PREFIX):]
        else:
            return

        cmd = cmd.lower().strip()

        if cmd not in config.cmds:
            return

        try:
            exec(config.cmds[cmd], locals())
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            msg = "\n\n"
            msg += (
                "<b>{0}</b>: <f x{1}{2}=\"8\">"
                "{4}<f x{1}{2}=\"{3}\">\n"
            ).format(
                exc_type.__name__,
                str(self.user.fontSize).rjust(2, "0"),
                self.user.fontColor,
                self.user.fontFace,
                html.escape(str(exc_value))
            )
            for frame in traceback.extract_tb(exc_traceback):
                filename = frame.filename
                if filename.startswith(config.CWD):
                    filename = "." + filename[len(config.CWD):]
                msg += "File <i>{}</i> line {}: {}\n".format(
                    html.escape(filename),
                    frame.lineno,
                    html.escape(frame.name)
                )
            room.message(msg, html=True)
            traceback.print_exc()
