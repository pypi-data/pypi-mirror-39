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

import subprocess
import sys


def gs_cmd_generator(
    input_file, output_file, gs_exec, quality, rasterize, nofont, papersize, verbose
):
    yield gs_exec
    if not rasterize:
        yield "-sDEVICE=pdfwrite"
    else:
        yield "-sDEVICE=pdfimage24"
    yield "-dCompatibilityLevel=1.4"
    yield f"-dPDFSETTINGS=/{quality}"
    if nofont:
        yield "-dNoOutputFonts"
    if papersize is not None:
        yield f"-sPAPERSIZE={papersize}"
        yield "-dPDFFitPage"
        yield "-dFIXEDMEDIA"
    if rasterize:
        factor = 4
        resolution = {"screen": 144, "ebook": 300, "printer": 600}[quality]
        yield f"-r{factor*resolution}"
        yield f"-dDownScaleFactor={factor}"
    yield "-dNOPAUSE"
    if not verbose:
        yield "-dQUIET"
        yield "-dBATCH"
    yield "-o"
    yield output_file
    yield input_file


def rewrite(
    input_file,
    output_file,
    gs_exec="gs",
    quality="ebook",
    rasterize=False,
    nofont=False,
    papersize=None,
    verbose=False,
    debug=False,
):
    """Rewrite pdf with Ghostcript

    :param input_file: input PDF file
    :param output_file: output PDF file
    :param gs_exec: Ghostcript executable (default: 'gs')
    :param quality: Ghostcript PDFSETTING profile (e.g. screen, ebook, printer)
            (default: ebook)
    :param rasterize: boolean to fore complete rasterization
    :param nofont: boolean to force conversion of all fonts to path
    :param papersize: if provided, resize the pdf to the given papersize
            (e.g. a4, a5, letter)
    :param verbose: boolean controling Ghoscript verbosity
    :param debug: print on stderr the Ghoscript command
    """

    gs_cmd = tuple(
        gs_cmd_generator(
            input_file,
            output_file,
            gs_exec=gs_exec,
            quality=quality,
            rasterize=rasterize,
            nofont=nofont,
            papersize=papersize,
            verbose=verbose,
        )
    )
    if debug:
        print(" ".join(repr(k) for k in gs_cmd), file=sys.stderr)
    subprocess.call(gs_cmd)
