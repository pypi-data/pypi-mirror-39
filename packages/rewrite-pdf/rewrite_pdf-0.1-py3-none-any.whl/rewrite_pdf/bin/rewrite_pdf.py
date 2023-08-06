#!/usr/bin/env python3

# Copyright (c) 2018, Jean-Benoist Leger <jb@leger.tf>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import argparse
import textwrap

import rewrite_pdf


def parseargs():
    parser = argparse.ArgumentParser(
        description="Rewrite pdf with ghostscript.",
        epilog=textwrap.dedent(
            """\
            Examples:
            compress a pdf with default config:
              %(prog)s input.pdf output.pdf
            compress a pdf with low quality:
              %(prog)s -q screen input.pdf output.pdf
            convert all fonts to paths (for a stupid printer):
              %(prog)s -n input.pdf output.pdf
            rasterize the pdf with printer quality (for a very stupid printer):
              %(prog)s -rq printer input.pdf output.pdf
            compress and resize a pdf to A5 format:
              %(prog)s -s a5 input.pdf output.pdf
            """
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--version", action="version", version=rewrite_pdf.__version__, help=argparse.SUPPRESS
    )
    parser.add_argument(
        "-e",
        "--exec",
        dest="gs_exec",
        nargs=1,
        default="gs",
        metavar="gs_exec",
        help="Ghostscript executable. (default: gs)",
    )
    parser.add_argument(
        "-q",
        "--quality",
        dest="quality",
        choices=("screen", "ebook", "printer"),
        default="ebook",
        help="Ghostscript quality profile. (default: ebook)",
    )
    parser.add_argument(
        "-s",
        "--size",
        "--resize",
        dest="papersize",
        help="Resize to the requested papersize."
        " Must be one of paper sizes known to Ghostscript. (e.g. a4, a5, letter...)",
    )
    nofont_or_rasterize = parser.add_mutually_exclusive_group()
    nofont_or_rasterize.add_argument(
        "-n",
        "--nofont",
        dest="nofont",
        action="store_true",
        help="Convert font to path.",
    )
    nofont_or_rasterize.add_argument(
        "-r",
        "--rasterize",
        dest="rasterize",
        action="store_true",
        help="Rasterize the content of the pdf.",
    )
    parser.add_argument("input", help="Input file", metavar="input_pdf")
    parser.add_argument("output", help="Output file", metavar="output_pdf")

    args = parser.parse_args()
    return args


def main():
    args = parseargs()
    rewrite_pdf.rewrite(
        args.input,
        args.output,
        gs_exec=args.gs_exec,
        quality=args.quality,
        rasterize=args.rasterize,
        nofont=args.nofont,
        papersize=args.papersize,
        verbose=args.verbose,
        debug=args.debug,
    )


if __name__ == "__main__":
    main()
