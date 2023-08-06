# -*- coding: utf-8 -*-
# :Project:   metapensiero.tool.tinject -- Configuration details
# :Created:   gio 21 apr 2016 18:22:20 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2018 Lele Gaifax
#

from ruamel.yaml import Loader, add_constructor, dump_all, load_all


def include(loader, node):
    path = loader.construct_scalar(node)
    fullpath = include.basedir / path
    return fullpath.read_text('utf-8')

add_constructor('!include', include, Loader=Loader)


class Config(object):
    @classmethod
    def from_yaml(cls, fname):
        include.basedir = fname.parent
        with fname.open() as stream:
            content = load_all(stream, Loader=Loader)
            globals = next(content)
            try:
                actions = next(content)
            except StopIteration:
                actions = globals
                globals = {}
        return cls(globals, actions)

    def __init__(self, globals, actions):
        self.globals = globals
        self.actions = actions

    def write(self, output):
        with output.open('w') as stream:
            dump_all([self.globals, self.actions], stream,
                     default_style="|",
                     default_flow_style=False)
