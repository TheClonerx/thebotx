import config
import ch
import html

note = args.partition(" ")[2]
args = args.split()
cuser = None if user.name[0] in "#!" else config.User(user.name)
lang = "en" if cuser is None else cuser.lang

if not cuser:
    msg = config.get_lang("en", "not_for_anons")
elif not args:
    msg = config.get_lang(lang, "missing_argument")
    arg = config.get_lang(lang, "argument_action")
    msg = msg.format(arg)
elif args[0].lower() == "add":
    if not args[1:]:
        msg = config.get_lang(lang, "missing_argument")
        arg = config.get_lang(lang, "argument_note")
        msg = msg.format(arg)
    else:
        cuser.add_note(note)
        note_n = cuser.get_notes_len()
        msg = config.get_lang(lang, "added_note")
        msg = msg.format(note_n)
elif args[0].lower() == "see":
    if not cuser.get_notes_len():
        msg = config.get_lang(lang, "doesnt_has_notes")
    elif not args[1:]:
        msg = config.get_lang(lang, "notes_see_page")
        see_n = config.get_lang(lang, "notes_see_n")
        page = cuser.get_notes(slice(0, 10))
        msg = msg.format(
            1, cuser.get_notes_len() // 10 + 1,
            "\n&nbsp; &nbsp; ".join(
                see_n.format(i + 1, html.escape(n)) for i, n in enumerate(page)
            )
        )
    elif not args[1].isnumeric():
        msg = config.get_lang(lang, "invalid_argument")
        arg = config.get_lang(lang, "invalid_argument_not_an_int")
        msg = msg.format(2, arg)
    else:
        page_n = int(args[1])
        if cuser.get_notes_len() // 10 + 1 < page_n:
            msg = config.get_lang(lang, "invalid_argument")
            arg = config.get_lang(lang, "invalid_argument_number_too_high")
            msg = msg.format(2, arg)
        elif page_n < 1:
            msg = config.get_lang(lang, "invalid_argument")
            arg = config.get_lang(lang, "invalid_argument_number_too_low")
            msg = msg.format(2, arg)
        else:
            pages = [
                cuser.get_notes(slice(i, i + 10)) for i in range(
                    0, cuser.get_notes_len(), 10
                )
            ]
            page = pages[page_n - 1]
            msg = config.get_lang(lang, "notes_see_page")
            see_n = config.get_lang(lang, "notes_see_n")
            msg = msg.format(page_n, len(pages), "\n&nbsp; &nbsp; ".join(
                see_n.format(
                    (page_n - 1) * 10 + i + 1, html.escape(n)
                ) for i, n in enumerate(page)
            ))
elif args[0].lower() == "del":
    if not cuser.get_notes_len():
        msg = config.get_lang(lang, "doesnt_has_notes")
    elif not args[1:]:
        msg = config.get_lang(lang, "missing_argument")
        arg = config.get_lang(lang, "argument_note_id")
        msg = msg.format(arg)
    elif not args[1].isnumeric():
        msg = config.get_lang(lang, "invalid_argument")
        arg = config.get_lang(lang, "invalid_argument_not_an_int")
        msg = msg.format(2, arg)
    else:
        note_n = int(args[1])
        if cuser.get_notes_len() < note_n:
            msg = config.get_lang(lang, "invalid_argument")
            arg = config.get_lang(lang, "invalid_argument_number_too_high")
            msg = msg.format(2, arg)
        elif note_n < 1:
            msg = config.get_lang(lang, "invalid_argument")
            arg = config.get_lang(lang, "invalid_argument_number_too_low")
            msg = msg.format(2, arg)
        else:
            cuser.del_note(note_n - 1)
            msg = config.get_lang(lang, "deleted_note")
            msg = msg.format(note_n)
elif args[0].lower() == "_see" and user.name in config.owners:
    if len(args) == 1:
        msg = config.get_lang(lang, "missing_argument")
        arg = config.get_lang(lang, "agument_user")
        msg = msg.format(arg)
    elif not args[1].isalnum():
        msg = config.get_lang(lang, "invalid_argument")
        arg = config.get_lang(lang, "invalid_argument_not_an_user")
        msg = msg.format(2, arg)
    elif not config.User(args[1]).get_notes_len():
        msg = config.get_lang(lang, "doesnt_has_notes")
        msg = msg.format(ch.User(args[1]).capser)
    elif not args[2:]:
        auser = config.User(args[1])
        page = auser.get_notes(slice(0, 10))
        msg = config.get_lang(lang, "notes__see_page")
        see_n = config.get_lang(lang, "notes_see_n")
        msg = msg.format(
            ch.User(args[1]).capser, 1, auser.get_notes_len() // 10 + 1,
            "\n&nbsp; &nbsp; ".join(
                see_n.format(i + 1, html.escape(n)) for i, n in enumerate(page)
            )
        )
    elif not args[2].isnumeric():
        msg = config.get_lang(lang, "invalid_argument")
        arg = config.get_lang(lang, "invalid_argument_not_an_int")
        msg = msg.format(3, arg)
    else:
        auser = config.User(args[1])
        page = int(args[2]) - 1
        pages = [
            auser.get_notes(slice(i, i + 10)) for i in range(
                0, auser.get_notes_len(), 10
            )
        ]
        if len(pages) < page + 1:
            msg = config.get_lang(lang, "invalid_argument")
            arg = config.get_lang(lang, "invalid_argument_number_too_high")
            msg = msg.format(3, arg)
        elif page < 0:
            msg = config.get_lang(lang, "invalid_argument")
            arg = config.get_lang(lang, "invalid_argument_number_too_low")
            msg = msg.format(3, arg)
        else:
            msg = config.get_lang(lang, "notes__see_page")
            see_n = config.get_lang(lang, "notes_see_n")
            msg = msg.format(
                ch.User(args[2]).capser, page + 1, len(pages),
                "\n&nbsp; &nbsp; ".join(
                    see_n.format(
                        page + i, html.escape(note)
                    ) for i, note in enumerate(pages[page])
                )
            )
else:
    msg = config.get_lang(lang, "invalid_argument")
    arg = config.get_lang(lang, "invalid_argument_action")
    msg = msg.format(1, arg)
room.message(msg, True)
