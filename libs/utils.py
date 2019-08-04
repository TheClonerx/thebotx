import sys
import time
import ch
import collections
import re

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
YEAR = 365.25 * DAY

DEFAULT_IMG = (
    b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x02\x00\x00d\x00d\x00\x00\xff\xec"
    b"\x00\x11Ducky\x00\x01\x00\x04\x00\x00\x00P\x00\x00\xff\xee\x00\x0eAdobe"
    b"\x00d\xc0\x00\x00\x00\x01\xff\xdb\x00\x84\x00\x02\x02\x02\x02\x02\x02"
    b"\x02\x02\x02\x02\x03\x02\x02\x02\x03\x04\x03\x02\x02\x03\x04\x05\x04\x04"
    b"\x04\x04\x04\x05\x06\x05\x05\x05\x05\x05\x05\x06\x06\x07\x07\x08\x07\x07"
    b"\x06\t\t\n\n\t\t\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c"
    b"\x0c\x01\x03\x03\x03\x05\x04\x05\t\x06\x06\t\r\x0b\t\x0b\r\x0f\x0e\x0e"
    b"\x0e\x0e\x0f\x0f\x0c\x0c\x0c\x0c\x0c\x0f\x0f\x0c\x0c\x0c\x0c\x0c\x0c\x0f"
    b"\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c"
    b"\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\xff\xc0\x00\x11\x08\x002\x002"
    b"\x03\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00d\x00\x01\x00\x03"
    b"\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x06\x07\x03"
    b"\x04\x08\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    b"\x00\x00\x10\x00\x01\x04\x02\x01\x03\x03\x04\x03\x00\x00\x00\x00\x00\x00"
    b"\x00\x02\x00\x01\x03\x04\x05\x06\x11!1\x13A\x12\x07Qa\x81\x14\"2R\x11"
    b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff"
    b"\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00?\x00\xd9\x10\x10\x10\x10"
    b"\x10\x10\x10\x10\x10]u\x9f\x8f\xb6}\xb2\"\xb5\x8b\xa4#HI\xc3\xf7\xac"
    b"\x1bG\x13\x93waw\xe5\xcb\x8f^\x19\xd0v6/\x8dv\xddf\xb1^\xbfDg\xa1\x1f"
    b"\x1ek\x95M\xa5\x00\xe7\xfd\xb7B\x16\xfb\xb8\xf1\xf7AB@@@@A\xa9\xe4>R"
    b"\xcbZ\xd6ij\xf8\xaa#\x84\x8e\xb0\xc5\x0b\xda\xa7)\xb4\x92E\x18\xf1\xec"
    b"\xe8\xcc\xec\xe6\xfdI\xd9\xfa\xfe]\x06\xc3\xa3C\x94\xd74l\xcd\xbd\xf6"
    b"\xc1\xb62\xc0\x14\x90P\xb8nr\x84$\x0e$\x0e\xc4\xee\xec\xf2;\xb30w\xe7"
    b"\xd3\x97A\xe4\xb4\x04\x04\x04\x04\x17\xaf\x8d\xce\xbc;\x8e*\xcd\x9cu\x9c"
    b"\xa8U\xf2\xcd\x1d:\x91y\xa5y\x022p&\x0e[\x9fk\xf0]\xfd\x10L|\xad\xb4\xe4"
    b"\xb3\xbb\x14\xf4\xa5\x0btq\xb8\xe1\x8b\xf5qV\x83\xc2`G\x10\x99\x1c\x91"
    b"\xf2\xff\x00\xc9\xdc\xba;\xbf\xf5\xe1\x06Z\x80\x80\x80\x80\x82\x7fZ\xd8"
    b"\xae\xea\xb9x3X\xf8\xa0\x9a\xd5q\x90\x02;\x02E\x1b\xb4\x82\xe0\xfc\xb0"
    b"\x10?g\xfa\xa0\xe3\xd8\xf3\xd76|\xcd\xcc\xe5\xf8\xe1\x86\xdd\xef\x1f\x96"
    b":\xecC\x1bx\xa3\x18\x9b\xda\xc4F\xfd\x81\xb9\xea\x82\x11\x01\x01\x01\x01"
    b"\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x07\xff\xd9"
)


class DotDict(dict):
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, val):
        self[attr] = val

    def __delattr__(self, attr):
        del self[attr]


def arguments(*args, **kwargs):
    args = ", ".join(repr(x) for x in args)
    kwargs = ", ".join("{x} = {y}".format(x, y) for x, y in kwargs.items())
    if args and kwargs:
        return "({}, {})".format(args, kwargs)
    return "({})".format(args or kwargs)


def event(func):
    def wraper(*args, **kwargs):
        # args[0] is self, the bot
        # print(func.__name__ + arguments(*args, **kwargs))
        to_print = time.strftime("%X ")
        to_print += func.__name__ + " "
        for arg in args[1:]:
            if isinstance(arg, ch.PM):
                to_print += "[PM] "
            elif isinstance(arg, ch.Room):
                to_print += "[{}] ".format(arg.name)
            elif isinstance(arg, ch._User):
                to_print += "<{}> ".format(arg.name)
            elif isinstance(arg, ch.Message):
                to_print += repr(arg.body)[1:-1]
            else:
                to_print += repr(arg)
        print(to_print)
        return func(*args, **kwargs)
    return wraper

Time = collections.namedtuple("Time", [
    "past", "years", "days", "hours", "minutes", "seconds"
])


def delta_time(when, now=None):
    if now is None:  # now could be 0
        now = time.time()
    delta = when - now
    past = delta < 0
    delta = abs(delta)

    years = int(delta / YEAR)
    days = int((delta % YEAR) / DAY)
    hours = int((delta % DAY) / HOUR)
    minutes = int((delta % HOUR) / MINUTE)
    seconds = int(delta % MINUTE)

    return Time(past, years, days, hours, minutes, seconds)


def str_delta(lang, delta):
    # i put it here to prevent recursions in the imports
    from config import get_lang
    text = []

    if delta.years == 1:
        text.append(get_lang(lang, "time_year").format(delta.years))
    elif delta.years:
        text.append(get_lang(lang, "time_years").format(delta.years))

    if delta.days == 1:
        text.append(get_lang(lang, "time_day").format(delta.days))
    elif delta.days:
        text.append(get_lang(lang, "time_days").format(delta.days))

    if delta.hours == 1:
        text.append(get_lang(lang, "time_hour").format(delta.hours))
    elif delta.hours:
        text.append(get_lang(lang, "time_hours").format(delta.hours))

    if delta.minutes == 1:
        text.append(get_lang(lang, "time_minute").format(delta.minutes))
    elif delta.minutes:
        text.append(get_lang(lang, "time_minutes").format(delta.minutes))

    if delta.seconds == 1:
        text.append(get_lang(lang, "time_second").format(delta.seconds))
    elif delta.seconds:
        text.append(get_lang(lang, "time_seconds").format(delta.seconds))

    if not text:
        return get_lang(lang, "time_now")

    if len(text) == 1:
        if delta.past:
            return get_lang(lang, "time_ago").format(text[0])
        else:
            return text[0]
    _and = get_lang(lang, "literaly_and")
    text = _and.format(", ".join(text[:-1]), text[-1])
    if delta.past:
        return get_lang(lang, "time_ago").format(text)
    else:
        return text


def is_room_or_user(name):
    return bool(re.match(r'[a-z0-9-]+', name, re.I))
