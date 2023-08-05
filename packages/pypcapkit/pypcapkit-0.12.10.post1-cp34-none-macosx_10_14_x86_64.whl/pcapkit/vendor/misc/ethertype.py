# -*- coding: utf-8 -*-

import collections
import contextlib
import csv
import os
import re

import requests

###############
# Macros
###############

NAME = 'EtherType'
DOCS = 'Ethertype IEEE 802 Numbers'
FLAG = 'isinstance(value, int) and 0x0000 <= value <= 0xFFFF'
LINK = 'https://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers-1.csv'

###############
# Processors
###############

page = requests.get(LINK)
data = page.text.strip().split('\r\n')

reader = csv.reader(data)
header = next(reader)
record = collections.Counter(map(lambda item: item[4],
                                 filter(lambda item: len(item[1].split('-')) != 2, reader)))


def rename(name, code):
    if record[name] > 1:
        name = f'{name} [0x{code}]'
    return name


reader = csv.reader(data)
header = next(reader)

enum = list()
miss = list()
for item in reader:
    name = item[4]
    rfcs = item[5]

    temp = list()
    for rfc in filter(None, re.split(r'\[|\]', rfcs)):
        if 'RFC' in rfc:
            temp.append(f'[{rfc[:3]} {rfc[3:]}]')
        else:
            temp.append(f'[{rfc}]')
    desc = re.sub(r'( )( )*', ' ',
                  f"# {''.join(temp)}".replace('\n', ' ')) if rfcs else ''

    try:
        code, _ = item[1], int(item[1], base=16)
        renm = re.sub(r'( )( )*', ' ', rename(name, code).replace('\n', ' '))

        pres = f"{NAME}[{renm!r}] = 0x{code}".ljust(76)
        sufs = f"\n{' '*80}{desc}" if len(pres) >= 80 else desc

        enum.append(f'{pres}{sufs}')
    except ValueError:
        start, stop = item[1].split('-')
        more = re.sub(r'\r*\n', ' ', desc, re.MULTILINE)

        miss.append(f'if 0x{start} <= value <= 0x{stop}:')
        if more:
            miss.append(f'    {more}')
        miss.append(
            f"    extend_enum(cls, '{name} [0x%s]' % hex(value)[2:].upper().zfill(4), value)")
        miss.append('    return cls(value)')

###############
# Defaults
###############

temp, FILE = os.path.split(os.path.abspath(__file__))
ROOT, STEM = os.path.split(temp)

ENUM = '\n    '.join(map(lambda s: s.rstrip(), enum))
MISS = '\n        '.join(map(lambda s: s.rstrip(), miss))


def LINE(NAME, DOCS, FLAG, ENUM, MISS): return f'''\
# -*- coding: utf-8 -*-

from aenum import IntEnum, extend_enum


class {NAME}(IntEnum):
    """Enumeration class for {NAME}."""
    _ignore_ = '{NAME} _'
    {NAME} = vars()

    # {DOCS}
    {ENUM}

    @staticmethod
    def get(key, default=-1):
        """Backport support for original codes."""
        if isinstance(key, int):
            return {NAME}(key)
        if key not in {NAME}._member_map_:
            extend_enum({NAME}, key, default)
        return {NAME}[key]

    @classmethod
    def _missing_(cls, value):
        """Lookup function used when value is not found."""
        if not ({FLAG}):
            raise ValueError('%r is not a valid %s' % (value, cls.__name__))
        {MISS}
        super()._missing_(value)
'''


with contextlib.suppress(FileExistsError):
    os.mkdir(os.path.join(ROOT, f'../const/{STEM}'))
with open(os.path.join(ROOT, f'../const/{STEM}/{FILE}'), 'w') as file:
    file.write(LINE(NAME, DOCS, FLAG, ENUM, MISS))
