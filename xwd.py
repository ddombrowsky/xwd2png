#!/usr/bin/env python3

from __future__ import division, print_function, unicode_literals

import re
import getopt
import sys
from xwdfile import xwd_open, binary

def main(argv=None):
    if argv is None:
        argv = sys.argv

    opts, args = getopt.getopt(argv[1:], 'i', ['info', 'raw'])

    options = [o for o,v in opts]

    if len(args) == 0:
        inp = binary(sys.stdin)
        out = binary(sys.stdout)
    else:
        inp = open(args[0], 'rb')
        out = None

    xwd = xwd_open(inp)

    if '-i' in options or '--info' in options:
        info = xwd.info()
        dprint(info)
        return 0

    if '--raw' in options:
        for row in xwd:
            print(*row)
        return 0

    if out is None:
        try:
            inp.name
        except AttributeError:
            out = "xwd2png_out.png"
        else:
            out = re.sub(r'(\..*|)$', '.png', inp.name)
            if out == inp.name:
                # avoid overwriting input,
                # if, for some reason,
                # input is mysteriously named: input.png
                output_name += '.png'

    format = xwd.uni_format()

    assert format == "RGB8"

    import png
    apng = png.from_array(xwd, "RGB;8")
    apng.save(out)

def dprint(o, indent=0):
    for k,v in sorted(o.items()):
        print(" "*indent, end="")
        if isinstance(v, dict):
            print(k+":")
            dprint(v, indent=indent+2)
            continue
        if 'mask' in k:
            v = "{:#x}".format(v)
        print(k, v)

if __name__ == '__main__':
    main()
