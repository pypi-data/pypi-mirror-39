from __future__ import absolute_import, division, print_function

from .cat import run as run_cat
from .grep import run as run_grep

class CatLaucher(object):
    @staticmethod
    def run(args):
        run_cat(args.input)

class GrepLauncher(object):
    @staticmethod
    def run(args):
        run_grep(
            args.inputs,
            args.pattern,
            args.e,
            args.f,
            args.v
        )
