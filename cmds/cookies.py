import config
import random
import time
import math
import html
import ch

args = args.split()
cuser = None if user.name[0] in "#!" else config.User(user.name)
lang = cuser.lang if cuser else "en"

nan, inf = math.nan, math.inf


def key(x):
    return x.cookies_amount


def cookies_str(u):
    if isinstance(u, config.User):
        c = u.cookies_amount
    else:
        c = int(u)
    return str(c)


if args and args[0].lower() == "top":
    if len(args) < 2:
        cursor = config.database.cursor()
        cursor.execute(
            "select name from users "
            "where cookies != 0 "
            "order by cookies desc "
            "limit 10"
        )
        top = [x[0] for x in cursor]
        cursor.close()
        top = [config.User(x) for x in top]
        top = [
            "{}: {} ({})".format(
                i + 1, ch.User(x.name).capser, cookies_str(x)
            ) for i, x in enumerate(top)
        ]
        msg = "\n\n" + config.get_lang(lang, "cookies_top").format(len(top))
        msg += "\n &nbsp; &nbsp;" + "\n &nbsp; &nbsp;".join(top)
    else:
        cursor = config.database.cursor()
        cursor.execute(
            "select name, cookies from users "
            "where cookies != 0 "
            "order by cookies desc"
        )
        top = list(cursor)
        cursor.close()
        for name, cookies in top:
            if name == args[1].lower():
                top = [u for u, c in top]
                index = top.index(args[1].lower())
                if index < 5:
                    start = 0
                    end = 10
                elif index > len(top) - 10:
                    start = len(top) - 10
                    end = -1
                else:
                    start = index - 5
                    end = index + 5
                top = [
                    "{}: {} ({})".format(
                        i + start + 1,
                        ch.User(x).capser if x != name else (
                            "<b>" + ch.User(x).capser + "</b>"
                        ),
                        cookies_str(config.User(x))
                    ) for i, x in enumerate(top[start:end])
                ]
                msg = "\n\n" + config.get_lang(lang, "cookies_top")
                msg = msg.format("{}-{}".format(start + 1, end))
                msg += "\n &nbsp; &nbsp;" + "\n &nbsp; &nbsp;".join(top)
                break
        else:
            msg = config.get_lang(lang, "doesnt_has_cookies")
            msg = msg.format(ch.User(args[1]).capser)
        
elif args and args[0].lower() == "see":
    if len(args) < 2:
        msg = config.get_lang(lang, "missing_argument")
        arg = config.get_lang(lang, "argument_user")
        msg = msg.format(arg)
    elif not cuser or not cuser.cookies_amount:
        msg = config.get_lang(lang, "doesnt_has_cookies")
        msg = msg.format(html.escape(args[1]))
    else:
        amount = cookies_str(config.User(args[1]))
        if amount == "0":
            msg = config.get_lang(lang, "doesnt_has_cookies")
            msg = msg.format(html.escape(args[1]))
        else:
            msg = config.get_lang(lang, "cookies_amount")
            msg = msg.format(ch.User(args[1]).capser, amount)
else:
    if not cuser:
        msg = config.get_lang("en", "not_for_anons")
    elif time.time() - cuser.cookies_time < 300:
        diff = 300 - (time.time() - cuser.cookies_time)
        msg = config.get_lang(lang, "wait_for_cookies")
        msg = msg.format(int(diff // 60), int(diff % 60))
    else:
        gained = random.randint(2, 10)
        cuser.cookies_amount += gained
        cuser.cookies_time = time.time()
        msg = config.get_lang(lang, "cookies_gained")
        msg = msg.format(gained, cookies_str(cuser))

room.message(msg, html=True)
