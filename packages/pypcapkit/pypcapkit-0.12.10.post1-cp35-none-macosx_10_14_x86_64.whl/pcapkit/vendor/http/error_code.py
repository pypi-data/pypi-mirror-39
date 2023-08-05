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

NAME = 'ErrorCode'
DOCS = 'HTTP/2 Error Code'
FLAG = 'isinstance(value, int) and 0x0000_0000 <= value <= 0xFFFF_FFFF'
LINK = 'https://www.iana.org/assignments/http2-parameters/error-code.csv'

###############
# Processors
###############

page = requests.get(LINK)
data = page.text.strip().split('\r\n')

reader = csv.reader(data)
header = next(reader)
record = collections.Counter(map(lambda item: item[1],
                                 filter(lambda item: len(item[0].split('-')) != 2, reader)))


def hexlify(code):
    temp = hex(code)[2:].upper().zfill(8)
    return f'0x{temp[:4]}_{temp[4:]}'


def rename(name, code):
    if record[name] > 1:
        return f'{name} [{code}]'
    return name


reader = csv.reader(data)
header = next(reader)

enum = list()
miss = list()
for item in reader:
    name = item[1]
    dscp = item[2]
    rfcs = item[3]

    temp = list()
    for rfc in filter(None, re.split(r'\[|\]', rfcs)):
        if 'RFC' in rfc:
            temp.append(f'[{rfc[:3]} {rfc[3:]}]')
        else:
            temp.append(f'[{rfc}]')
    desc = f" {''.join(temp)}" if rfcs else ''
    dscp = f' {dscp}' if dscp else ''

    try:
        temp = int(item[0], base=16)
        code = hexlify(temp)
        renm = rename(name, code)

        pres = f"{NAME}[{renm!r}] = {code}".ljust(76)
        sufs = f'#{desc}{dscp}' if desc or dscp else ''

        enum.append(f'{pres}{sufs}')
    except ValueError:
        start, stop = map(lambda s: int(s, base=16), item[0].split('-'))

        miss.append(f'if {hexlify(start)} <= value <= {hexlify(stop)}:')
        if desc or dscp:
            miss.append(f'#{desc}{dscp}')
        miss.append('    temp = hex(value)[2:].upper().zfill(8)')
        miss.append(
            f"    extend_enum(cls, '{name} [0x%s]' % (temp[:4]+'_'+temp[4:]), value)")
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
