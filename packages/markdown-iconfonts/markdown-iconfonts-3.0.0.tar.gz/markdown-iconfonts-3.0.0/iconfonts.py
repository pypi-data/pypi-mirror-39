"""
IconFonts Extension for Python-Markdown
"""

import markdown
import re

from markdown.util import etree
from markdown.inlinepatterns import InlineProcessor


class IconFontsExtension(markdown.extensions.Extension):
    """ IconFonts Extension for Python-Markdown. """

    def __init__(self, **kwargs):

        self.config = {
            "prefix": ["icon-", "Custom class prefix."],
            "base": ["", "Base class added to each icon"],
            "prefix_base_pairs": [{}, "Prefix/base pairs"],
        }

        super(IconFontsExtension, self).__init__(**kwargs)

    def add_inline(self, md, name, klass, re, config, index):
        pattern = klass(re, md, config)
        md.inlinePatterns.register(pattern, name, index)


    def extendMarkdown(self, md):
        config = self.getConfigs()

        # Change prefix to what they had the in the config
        # Capture "&icon-namehere;" or "&icon-namehere:2x;"
        # or "&icon-namehere:2x,muted;"
        # https://www.debuggex.com/r/weK9ehGY0HG6uKrg
        prefix = config["prefix"]
        icon_regex_start = r"&"
        icon_regex_end = r"(?P<name>[a-zA-Z0-9-]+)(:(?P<mod>[a-zA-Z0-9-]+(,[a-zA-Z0-9-]+)*)?(:(?P<user_mod>[a-zA-Z0-9-]+(,[a-zA-Z0-9-]+)*)?)?)?;"
        #                  ^---------------------^^ ^                    ^--------------^ ^ ^ ^                         ^--------------^ ^ ^ ^
        #                                         | +-------------------------------------+ | +------------------------------------------+ | |
        #                                         |                                         +----------------------------------------------+ |
        #                                         +------------------------------------------------------------------------------------------+
        # This is the full regex we use. Only reason we have pieces above is to easily change the prefix to something custom
        icon_regex = "".join([icon_regex_start, prefix, icon_regex_end])

        current_prio = 10
        # _idx = md.inlinePatterns.get_index_for_name("reference")
        prio = next(
            (
                prio.priority
                for prio in md.inlinePatterns._priority
                if prio.name == "reference"
            )
        )
        if prio:
            current_prio = prio + 10

        # Register the global one
        self.add_inline(
            md, "iconfonts", IconFontsPattern, icon_regex, config, current_prio
        )

        # Register each of the pairings
        for _prefix, _base in config["prefix_base_pairs"].items():

            _prefix_base = _prefix if _prefix[-1] != "-" else _prefix[:-1]

            icon_regex = "".join([icon_regex_start, _prefix, icon_regex_end])

            self.add_inline(
                md,
                "iconfonts_{}".format(_prefix_base),
                IconFontsPattern,
                icon_regex,
                {"prefix": _prefix, "base": _base},
                current_prio,
            )



class IconFontsPattern(InlineProcessor):
    """ Return a <i> element with the necessary classes"""

    def __init__(self, pattern, md, config):
        super(IconFontsPattern, self).__init__(pattern, md)

        self.config = config

    def handleMatch(self, match, data):
        # The dictionary keys come from named capture groups in the regex
        match_dict = match.groupdict()

        el = etree.Element("i")

        base = self.config["base"]
        prefix = self.config["prefix"]

        icon_class_name = match_dict.get("name")

        # Mods are modifier classes. The syntax in the markdown is:
        # "&icon-namehere:2x;" and with multiple "&icon-spinner:2x,spin;"
        mod_classes_string = ""
        if match_dict.get("mod"):
            # Make a string with each modifier like: "fa-2x fa-spin"
            mod_classes_string = " ".join(
                "{}{}".format(prefix, c)
                for c in match_dict.get("mod").split(",")
                if c
            )

        # User mods are modifier classes that shouldn't be prefixed with
        # prefix. The syntax in the markdown is:
        # "&icon-namehere::red;" and with multiple "&icon-spinner::red,bold;"
        user_mod_classes_string = ""
        if match_dict.get("user_mod"):
            # Make a string with each modifier like "red bold"
            user_mod_classes_string = " ".join(
                uc for uc in match_dict.get("user_mod").split(",") if uc
            )

        if prefix != "":
            icon_class = "{}{}".format(prefix, icon_class_name)
        else:
            icon_class = icon_class_name

            # Add the icon classes to the <i> element
        classes = "{} {} {} {}".format(
            base, icon_class, mod_classes_string, user_mod_classes_string
        )

        # Clean up classes
        classes = classes.strip()
        classes = re.sub(r"\s{2,}", " ", classes)

        el.set("class", classes)

        # This is for accessibility and text-to-speech browsers
        # so they don't try to read it
        el.set("aria-hidden", "true")

        return el, match.start(0), match.end(0)


def makeExtension(*args, **kwargs):
    return IconFontsExtension(**kwargs)
