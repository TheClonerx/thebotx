import json
import os
import sys
import copy
import traceback
import mysql.connector
from utils import DotDict
import ch

auth = {}
cmds = {}
langs = {}
owners = []

default_room = DotDict()
default_user = DotDict()

CWD = os.getcwd()

database = None


class User:
    _users = {}

    def __new__(cls, name):
        name = name.lower()
        if name in cls._users:
            return cls._users[name]
        self = super().__new__(cls)
        self.__name = name
        self.cookies_time = 0
        if name[0] not in "!#":
            assert database is not None
            cursor = database.cursor()
            cursor.execute(
                "select 1 from users where name = %s",
                (name,)
            )
            if not cursor.fetchone():
                cursor.execute(
                    "insert into users (name) values "
                    "(%s)",
                    (name,)
                )
                database.commit()
            cursor.close()
            cls._users[name] = self
        return self

    @property
    def name(self):
        return self.__name

    @property
    def cookies_amount(self):
        if self.__name[0] in "!#":
            return 0
        cursor = database.cursor()
        cursor.execute(
            "select cookies from users "
            "where name = %s",
            (self.__name,)
        )
        ret = cursor.fetchone()[0]
        cursor.close()
        return ret

    @cookies_amount.setter
    def cookies_amount(self, val):
        if self.__name[0] in "!#":
            return
        assert isinstance(val, (int, float))
        if isinstance(val, float):
            val = int(val)
        cursor = database.cursor()
        cursor.execute(
            "update users "
            "set cookies = %s "
            "where name = %s",
            (val, self.__name)
        )
        database.commit()

    @property
    def prefix(self):
        if self.__name[0] in "!#":
            return default_user["prefix"]
        cursor = database.cursor()
        cursor.execute(
            "select prefix from users "
            "where name = %s",
            (self.__name,)
        )
        ret = cursor.fetchone()[0]
        cursor.close()
        return ret

    @prefix.setter
    def prefix(self, val):
        if self.__name[0] in "!#":
            return
        assert isinstance(val, str)
        cursor = database.cursor()
        cursor.execute(
            "update users "
            "set prefix = %s "
            "where name = %s",
            (val, self.__name)
        )
        database.commit()

    @property
    def lang(self):
        if self.__name[0] in "!#":
            return default_user["lang"]
        cursor = database.cursor()
        cursor.execute(
            "select lang from users "
            "where name = %s",
            (self.__name,)
        )
        ret = cursor.fetchone()[0]
        cursor.close()
        return ret

    @lang.setter
    def lang(self, val):
        if self.__name[0] in "!#":
            return
        assert isinstance(val, str)
        cursor = database.cursor()
        cursor.execute(
            "update users "
            "set lang = %s "
            "where name = %s",
            (val, self.__name)
        )
        database.commit()

    def get_notes(self, index=None):
        if self.__name[0] in "!#":
            return list()
        if index is None:
            index = slice(None)
        assert isinstance(index, (int, slice))
        cursor = database.cursor()
        cursor.execute(
            "select content from notes "
            "where user = %s",
            (self.__name,)
        )
        return list(x[0] for x in cursor)[index]

    def get_notes_len(self):
        if self.__name[0] in "!#":
            return 0
        cursor = database.cursor()
        cursor.execute(
            "select count(*) from notes "
            "where user = %s",
            (self.__name,)
        )
        return cursor.fetchone()[0]

    def del_note(self, index):
        if self.__name[0] in "!#":
            return
        assert isinstance(index, int)
        cursor = database.cursor()
        cursor.execute(
            "select id from notes "
            "where user = %s",
            (self.__name,)
        )
        note_ids = list(x[0] for x in cursor)
        note_id = note_ids[index]
        cursor.execute(
            "delete from notes "
            "where id = %s",
            (note_id,)
        )
        database.commit()

    def add_note(self, note):
        if self.__name[0] in "!#":
            return
        assert isinstance(note, str)
        cursor = database.cursor()
        cursor.execute(
            "insert into notes (user, content) "
            "values (%s, %s)",
            (self.__name, note)
        )
        database.commit()

    def __repr__(self):
        return "<config for user %s>" % self.__name


class _RoomMetaclass(type):
        @property
        def room_names(cls):  # this is a `class property`
            cursor = database.cursor()
            cursor.execute("select name from rooms")
            ret = list(x[0] for x in cursor)
            if "_default" in ret:
                ret.remove("_default")
            return ret


class Room(metaclass=_RoomMetaclass):
    _rooms = {}

    def __new__(cls, name):
        name = name.lower()
        if name in cls._rooms:
            return cls._rooms[name]
        assert database is not None
        cursor = database.cursor()
        cursor.execute(
            "select 1 from rooms where name = %s",
            (name,)
        )
        if not cursor.fetchone():
            cursor.execute(
                "insert into rooms (name) values "
                "(%s)",
                (name,)
            )
            database.commit()
        self = super().__new__(cls)
        self.__name = name
        cls._rooms[name] = self
        return self

    @classmethod
    def del_room(cls, name):
        assert isinstance(name, str)
        name = name.lower()
        cursor = database.cursor()
        cursor.execute(
            "delete from rooms "
            "where name = %s",
            (name,)
        )
        database.commit()
        if name in cls._rooms:
            del cls._rooms[name]

    @property
    def name(self):
        return self.__name

    @property
    def blocked(self):
        cursor = database.cursor()
        cursor.execute(
            "select blocked from rooms "
            "where name = %s",
            (self.__name,)
        )
        return bool(cursor.fetchone()[0])

    @blocked.setter
    def blocked(self, val):
        assert isinstance(val, bool)
        cursor = database.cursor()
        cursor.execute(
            "update rooms "
            "set blocked = %s "
            "where name = %s",
            (int(val), self.__name)
        )
        database.commit()

    @property
    def channels(self):
        cursor = database.cursor()
        cursor.execute(
            "select channels from rooms "
            "where name = %s",
            (self.__name,)
        )
        channels = cursor.fetchone()[0]
        return tuple(x for x, y in ch.Channels.items() if channels & y and y)

    @channels.setter
    def channels(self, val):
        assert isinstance(val, (tuple, int))
        if isinstance(val, tuple):
            v = 0
            for x in val:
                v |= ch.Channels[x.lower()]
            val = v
            del v
        cursor = database.cursor()
        cursor.execute(
            "update rooms "
            "set channels = %s "
            "where name = %s",
            (val, self.__name)
        )
        database.commit()

    def __repr__(self):
        return "<config for room %s>" % self.__name


def connect_db():
    global database
    if not auth:
        load_auth()
    database = mysql.connector.connect(
        user=auth["name"].lower(),
        password=auth["password"],
        database=auth["name"].lower(),
        host="raspberry"
    )

def disconnect_db():
    """MAKE SURE TO COMMIT CHANGES FIRST"""
    global database
    database.close()
    database = None


def load_default_user():
    default_user.clear()
    assert database is not None
    cur = database.cursor(dictionary=True)
    cur.execute("select * from users where name = '_default'")
    du = cur.fetchone()
    cur.close()
    assert du is not None
    del du["name"]
    default_user.update(du)


def load_default_room():
    default_room.clear()
    assert database is not None
    cur = database.cursor(dictionary=True)
    cur.execute("select * from rooms where name = '_default'")
    dr = cur.fetchone()
    cur.close()
    assert dr is not None
    del dr["name"]
    default_room.update(dr)


def load_auth():
    auth.clear()
    with open("config/auth.json") as file:
        auth.update(json.load(file))


def load_owners():
    owners.clear()
    with open("config/owners.txt") as file:
        for line in file:
            owners.extend(x.lower() for x in line.split())


def load_langs():
    langs.clear()
    for path in os.scandir("langs/"):
        lang = os.path.splitext(os.path.split(path.path)[1])[0]
        with open(path.path, encoding="utf-8") as file:
            langs[lang] = json.load(file)


def load_cmds():
    cmds.clear()
    for path in os.listdir("cmds"):
        path = os.path.join("cmds", path)
        cmd = os.path.splitext(os.path.split(path)[1])[0]
        with open(path, encoding="utf-8") as file:
            try:
                cmds[cmd] = compile(
                    file.read(), "<command " + cmd + ">", "exec"
                )
            except:
                msg = "Error loading cmd {}.\n"
                msg = msg.format(cmd)
                print(msg, file=sys.stderr)
                traceback.print_exc(file=sys.stderr)


def save_auth():
    with open("config/auth.json", "w") as file:
        json.dump(auth, file)


def save_owners(owners_per_line=5):
    with open("config/owners.txt", "w") as file:
        for i, owner in enumerate(owners):
            file.write(owner)
            if (i + 1) % owners_per_line == 0:
                file.write("\n")
            else:
                file.write(" ")


def load_all():
    load_auth()
    load_langs()
    load_owners()
    load_cmds()
    load_default_user()
    load_default_room()


def save_all():
    os.chdir(CWD)
    save_owners()
    save_auth()


def get_lang(lang, id):
    if lang in langs and id in langs[lang]:
        return langs[lang][id]
    return "langs.{}.{}".format(lang, id)
