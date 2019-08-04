import platform
import sys
import config

lang = config.User(user.name).lang

python = platform.python_implementation() + " " + platform.python_version()
system = platform.system() + " " + platform.release()

if sys.platform.startswith("linux"):
    distro_name, distro_ver, distro_id = platform.linux_distribution()
    system += " (" + distro_name + " " + distro_ver + ")"

if hasattr(self, "start_time"):
    import utils

    delta = utils.delta_time(self.start_time)
    start_time = utils.str_delta(lang, delta)
else:
    start_time = None

msg = config.get_lang(lang, "platform").format(system)
msg += "\n" + config.get_lang(lang, "python").format(python)

if start_time:
    msg += "\n" + config.get_lang(lang, "start_time").format(start_time)

room.message(msg)
