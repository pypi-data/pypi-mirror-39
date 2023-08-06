#!/usr/bin/env python

from __future__ import print_function

"""
Pandoc filter to process code blocks with class "plantuml" into
plant-generated images.
Needs `plantuml.jar` from http://plantuml.com/.
"""

import os
import sys
import subprocess
import re

from pandocfilters import toJSONFilter, Para, Image, RawBlock
from pandocfilters import get_filename4code, get_caption, get_extension

PLANTUML_BIN = os.environ.get('PLANTUML_BIN', 'plantuml')

pattern = re.compile('%{(.*)\}$')

def plantuml(key, value, format_, meta):

    if key == 'Header':
        if 'tikz'in (str(meta)):
            os.environ["PLANTUML_LATEX_EXPORT"] = 'latex'

    if key == 'CodeBlock':
        if os.getenv("DEBUG", "f").lower() in ("1", "true"):
            print("plantuml", key, value, format_, meta)

        [[ident, classes, keyvals], code] = value

        if "plantuml" in classes:
            caption, typef, keyvals = get_caption(keyvals)

            if "PLANTUML_LATEX_EXPORT" in os.environ:
                latex_img_format = "latex"
            else:
                latex_img_format = "eps"

            filename = get_filename4code("plantuml", code)
            filetype = get_extension(format_, "png", html="svg", latex=latex_img_format, beamer=latex_img_format)

            src = filename + '.uml'
            dest = filename + '.' + filetype

            if not os.path.isfile(dest):
                txt = code.encode(sys.getfilesystemencoding())
                if not txt.startswith(b"@start"):
                    txt = b"@startuml\n" + txt + b"\n@enduml\n"
                with open(src, "wb") as f:
                    f.write(txt)
                subprocess.check_call(PLANTUML_BIN.split() + ["-t" + filetype, src])
                sys.stderr.write('Created image ' + dest + '\n')
            if (filetype == "latex") and (latex_img_format == 'latex'):
                latex = open(dest).read()
                return RawBlock('latex', latex.split("\\begin{document}")[-1].split("\\end{document}")[0])
            else:
                return Para([Image([ident, [], keyvals], caption, [dest, typef])])


def main():
    toJSONFilter(plantuml)


if __name__ == "__main__":
    main()
