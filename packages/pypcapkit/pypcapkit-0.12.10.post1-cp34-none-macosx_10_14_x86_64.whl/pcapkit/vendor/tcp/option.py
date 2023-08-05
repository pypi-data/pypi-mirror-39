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

T, F = True, False
nm_len, op_len = None, None

NAME = 'Option'
DOCS = 'TCP Option Kind Numbers'
FLAG = 'isinstance(value, int) and 0 <= value <= 255'
LINK = 'https://www.iana.org/assignments/tcp-parameters/tcp-parameters-1.csv'
DATA = {                             # # kind  length  type  process  comment            name
    0:  (F, 'eool'),                 # #   0      -      -      -                [RFC 793] End of Option List
    1:  (F, 'nop'),                  # #   1      -      -      -                [RFC 793] No-Operation
    2:  (T, 'mss', nm_len, 1),       # #   2      4      H      1                [RFC 793] Maximum Segment Size
    3:  (T, 'ws', nm_len, 1),        # #   3      3      B      1                [RFC 7323] Window Scale
    4:  (T, 'sackpmt', nm_len),      # #   4      2      ?      -       True     [RFC 2018] SACK Permitted
    5:  (T, 'sack', op_len, 0),      # #   5      N      P      0      2+8*N     [RFC 2018] SACK
    6:  (T, 'echo', nm_len, 0),      # #   6      6      P      0                [RFC 1072][RFC 6247] Echo
    7:  (T, 'echore', nm_len, 0),    # #   7      6      P      0                [RFC 1072][RFC 6247] Echo Reply
    8:  (T, 'ts', nm_len, 2),        # #   8     10     II      2                [RFC 7323] Timestamps
    9:  (T, 'poc', nm_len),          # #   9      2      ?      -       True     [RFC 1693][RFC 6247] POC Permitted
    10: (T, 'pocsp', nm_len, 3),     # #  10      3    ??P      3                [RFC 1693][RFC 6247] POC-Serv Profile
    11: (T, 'cc', nm_len, 0),        # #  11      6      P      0                [RFC 1693][RFC 6247] Connection Count
    12: (T, 'ccnew', nm_len, 0),     # #  12      6      P      0                [RFC 1693][RFC 6247] CC.NEW
    13: (T, 'ccecho', nm_len, 0),    # #  13      6      P      0                [RFC 1693][RFC 6247] CC.ECHO
    14: (T, 'chkreq', nm_len, 4),    # #  14      3      B      4                [RFC 1146][RFC 6247] Alt-Chksum Request
    15: (T, 'chksum', nm_len, 0),    # #  15      N      P      0                [RFC 1146][RFC 6247] Alt-Chksum Data
    19: (T, 'sig', nm_len, 0),       # #  19     18      P      0                [RFC 2385] MD5 Signature Option
    27: (T, 'qs', nm_len, 5),        # #  27      8      P      5                [RFC 4782] Quick-Start Response
    28: (T, 'timeout', nm_len, 6),   # #  28      4      P      6                [RFC 5482] User Timeout Option
    29: (T, 'ao', nm_len, 7),        # #  29      N      P      7                [RFC 5925] TCP Authentication Option
    30: (T, 'mp', nm_len, 8),        # #  30      N      P      8                [RFC 6824] Multipath TCP
    34: (T, 'fastopen', nm_len, 0),  # #  34      N      P      0                [RFC 7413] Fast Open
}

###############
# Processors
###############

page = requests.get(LINK)
data = page.text.strip().split('\r\n')

reader = csv.reader(data)
header = next(reader)
record = collections.Counter(map(lambda item: item[2], reader))


def rename(name, code, *, original):
    if record[original] > 1:
        return f'{name} [{code}]'
    return name


reader = csv.reader(data)
header = next(reader)

enum = list()
miss = [
    "extend_enum(cls, 'Unassigned [%d]' % value, value)",
    'return cls(value)'
]
for item in reader:
    dscp = item[2]
    rfcs = item[3]

    temp = list()
    for rfc in filter(None, re.split(r'\[|\]', rfcs)):
        if re.match(r'\d+', rfc):
            continue
        if 'RFC' in rfc:
            temp.append(f'[{rfc[:3]} {rfc[3:]}]')
        else:
            temp.append(f'[{rfc}]')
    desc = f"# {''.join(temp)}" if rfcs else ''
    name = dscp.split(' (')[0]

    try:
        code, _ = item[0], int(item[0])
        name = DATA.get(int(code), (None, str()))[1].upper() or name
        renm = rename(name or 'Unassigned', code, original=dscp)

        pres = f"{NAME}[{renm!r}] = {code}".ljust(76)
        sufs = re.sub(r'\r*\n', ' ', desc, re.MULTILINE)

        enum.append(f'{pres}{sufs}')
    except ValueError:
        start, stop = item[0].split('-')
        more = re.sub(r'\r*\n', ' ', desc, re.MULTILINE)

        miss.append(f'if {start} <= value <= {stop}:')
        if more:
            miss.append(f'    {more}')
        miss.append(f"    extend_enum(cls, '{name} [%d]' % value, value)")
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
