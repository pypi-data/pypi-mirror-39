"""Dead simple reporting library

This library provides simple way how to generate
arbitrary documents, 

"""

import jinja2
import logging
import sys
import os

log = logging.getLogger('report')


def parse_text_fields(s, start='"""!', end='"""'):

    lines = []
    isin = False
    for i, line in enumerate(s.split('\n')):
        if line.startswith(start):
            isin = True
            log.debug('Text block start at %d', i+1)
        elif line.startswith(end):
            isin = False
            log.debug('Text block end at %d', i+1)
        elif isin:
            lines.append(line)
    return '\n'.join(lines)


def generate(text=None, data={}):
    src = sys.argv[0]
    log.debug('Source file: ', src)

    # read the whole file
    if text is None:
        with open(src, 'r') as f:
            content = f.read()

        # filter text blocks
        text = parse_text_fields(content)

    # prepare template
    tpl = jinja2.Template(text)

    # render template
    out = tpl.render(**data)
    return out


class Report(dict):

    def __init__(self, outdir='.'):
        super(Report, self).__init__()
        self.outdir = outdir

    def add_data(self, **kvargs):
        """Add data as key value pairs."""
        self.update(kvargs)

    def add_path(self, filename, key=None):
        """
        Add relative path, key is the key used in text,
        returns path wher the figure should be saved.
        """

        # create missing subdirectory
        subdir = os.path.dirname(filename)
        path = os.path.join(self.outdir, subdir)
        if not os.path.isdir(path):
            os.makedirs(path)

        path = os.path.join(self.outdir, filename)
        log.debug('save path: %s for key %s', path, key)

        if key is not None:
            self[key] = filename

        return path

    def generate(self, text=None, data={}):
        """Parse text section and generate the report."""
        self.add_data(**data)
        out = generate(text=text, data=self)
        return out

