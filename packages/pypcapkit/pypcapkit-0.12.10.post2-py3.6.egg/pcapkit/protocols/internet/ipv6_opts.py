# -*- coding: utf-8 -*-
"""destination options for IPv6

`pcapkit.protocols.internet.ipv6_opts` contains
`IPv6_Opts` only, which implements extractor for
Destination Options for IPv6 (IPv6-Opts), whose structure
is described as below.

+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Next Header  |  Hdr Ext Len  |                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+                               +
|                                                               |
.                                                               .
.                            Options                            .
.                                                               .
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

"""
import datetime
import ipaddress

from pcapkit.const.ipv6.option import Option as _OPT_TYPE
from pcapkit.const.ipv6.qs_function import QS_Function as _QS_FUNC
from pcapkit.const.ipv6.router_alert import RouterAlert as _ROUTER_ALERT
from pcapkit.const.ipv6.seed_id import SeedID as _IPv6_Opts_SEED
from pcapkit.const.ipv6.tagger_id import TaggerId as _TID_TYPE
from pcapkit.corekit.infoclass import Info
from pcapkit.protocols.internet.internet import Internet
from pcapkit.utilities.exceptions import ProtocolError, UnsupportedCall

__all__ = ['IPv6_Opts']

# IPv6_Opts Unknown Option Actions
_IPv6_Opts_ACT = {
    '00': 'skip over this option and continue processing the header',
    '01': 'discard the packet',
    '10': 'discard the packet and, regardless of whether or not the'
          "packet's Destination Address was a multicast address, send an"
          "ICMP Parameter Problem, Code 2, message to the packet's"
          'Source Address, pointing to the unrecognized Option Type',
    '11': "discard the packet and, only if the packet's Destination"
          'Address was not a multicast address, send an ICMP Parameter'
          "Problem, Code 2, message to the packet's Source Address,"
          'pointing to the unrecognized Option Type',
}

# IPv6_Opts Options
_IPv6_Opts_OPT = {
    0x00: ('pad', 'Pad1'),                                                  # [RFC 8200] 0
    0x01: ('pad', 'PadN'),                                                  # [RFC 8200]
    0x04: ('tun', 'Tunnel Encapsulation Limit'),                            # [RFC 2473] 1
    0x05: ('ra', 'Router Alert'),                                           # [RFC 2711] 2
    0x07: ('calipso', 'Common Architecture Label IPv6 Security Option'),    # [RFC 5570]
    0x08: ('smf_dpd', 'Simplified Multicast Forwarding'),                   # [RFC 6621]
    0x0F: ('pdm', 'Performance and Diagnostic Metrics'),                    # [RFC 8250] 10
    0x26: ('qs', 'Quick-Start'),                                            # [RFC 4782][RFC Errata 2034] 6
    0x63: ('rpl', 'Routing Protocol for Low-Power and Lossy Networks'),     # [RFC 6553]
    0x6D: ('mpl', 'Multicast Protocol for Low-Power and Lossy Networks'),   # [RFC 7731]
    0x8B: ('ilnp', 'Identifier-Locator Network Protocol Nonce'),            # [RFC 6744]
    0x8C: ('lio', 'Line-Identification Option'),                            # [RFC 6788]
    0xC2: ('jumbo', 'Jumbo Payload'),                                       # [RFC 2675]
    0xC9: ('home', 'Home Address'),                                         # [RFC 6275]
    0xEE: ('ip_dff', 'Depth-First Forwarding'),                             # [RFC 6971]
}

# IPv6_Opts Unknown Option Descriptions
_IPv6_Opts_NULL = {
    0x1E: 'RFC3692-style Experiment',                               # [RFC 4727]
    0x3E: 'RFC3692-style Experiment',                               # [RFC 4727]
    0x4D: 'Deprecated',                                             # [RFC 7731]
    0x5E: 'RFC3692-style Experiment',                               # [RFC 4727]
    0x7E: 'RFC3692-style Experiment',                               # [RFC 4727]
    0x8A: 'Endpoint Identification',                                # DEPRECATED
    0x9E: 'RFC3692-style Experiment',                               # [RFC 4727]
    0xBE: 'RFC3692-style Experiment',                               # [RFC 4727]
    0xDE: 'RFC3692-style Experiment',                               # [RFC 4727]
    0xFE: 'RFC3692-style Experiment',                               # [RFC 4727]
}


def _IPv6_Opts_PROC(abbr):
    """IPv6_Opts option process functions."""
    return eval(f'lambda self, code, *, desc: self._read_opt_{abbr}(code, desc=desc)')


class IPv6_Opts(Internet):
    """This class implements Destination Options for IPv6.

    Properties:
        * name -- str, name of corresponding protocol
        * info -- Info, info dict of current instance
        * alias -- str, acronym of corresponding protocol
        * layer -- str, `Internet`
        * length -- int, header length of corresponding protocol
        * protocol -- str, name of next layer protocol
        * protochain -- ProtoChain, protocol chain of current instance

    Methods:
        * read_ipv6_opts -- read Destination Options for IPv6 (IPv6-Opts)

    Attributes:
        * _file -- BytesIO, bytes to be extracted
        * _info -- Info, info dict of current instance
        * _protos -- ProtoChain, protocol chain of current instance

    Utilities:
        * _read_protos -- read next layer protocol type
        * _read_fileng -- read file buffer
        * _read_unpack -- read bytes and unpack to integers
        * _read_binary -- read bytes and convert into binaries
        * _read_packet -- read raw packet data
        * _decode_next_layer -- decode next layer protocol type
        * _import_next_layer -- import next layer protocol extractor

    """
    ##########################################################################
    # Properties.
    ##########################################################################

    @property
    def name(self):
        """Name of current protocol."""
        return 'IPv6 Hop-by-Hop Options'

    @property
    def alias(self):
        """Acronym of corresponding protocol."""
        return 'IPv6-Opts'

    @property
    def length(self):
        """Header length of current protocol."""
        return self._info.length  # pylint: disable=E1101

    @property
    def payload(self):
        """Payload of current instance."""
        if self._extf:
            raise UnsupportedCall(f"'{self.__class__.__name__}' object has no attribute 'payload'")
        return self._next

    @property
    def protocol(self):
        """Name of next layer protocol."""
        return self._info.next  # pylint: disable=E1101

    ##########################################################################
    # Methods.
    ##########################################################################

    def read_ipv6_opts(self, length, extension):
        """Read Destination Options for IPv6.

        Structure of IPv6-Opts header [RFC 8200]:
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |  Next Header  |  Hdr Ext Len  |                               |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+                               +
            |                                                               |
            .                                                               .
            .                            Options                            .
            .                                                               .
            |                                                               |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

            Octets      Bits        Name                    Description
              0           0     opt.next                Next Header
              1           8     opt.length              Header Extensive Length
              2          16     opt.options             Options

        """
        if length is None:
            length = len(self)

        _next = self._read_protos(1)
        _hlen = self._read_unpack(1)
        # _opts = self._read_fileng(_hlen*8+6)

        ipv6_opts = dict(
            next=_next,
            length=(_hlen + 1) * 8,
        )

        options = self._read_ipv6_opts_options(_hlen * 8 + 6)
        ipv6_opts['options'] = options[0]       # tuple of option acronyms
        ipv6_opts.update(options[1])            # merge option info to buffer

        length -= ipv6_opts['length']
        ipv6_opts['packet'] = self._read_packet(header=ipv6_opts['length'], payload=length)

        if extension:
            self._protos = None
            return ipv6_opts
        return self._decode_next_layer(ipv6_opts, _next, length)

    ##########################################################################
    # Data models.
    ##########################################################################

    def __init__(self, _file, length=None, *, extension=False, **kwargs):
        self._file = _file
        self._extf = extension
        self._info = Info(self.read_ipv6_opts(length, extension))

    def __length_hint__(self):
        return 2

    ##########################################################################
    # Utilities.
    ##########################################################################

    def _read_opt_type(self, kind):
        """Read option type field.

        Positional arguments:
            * kind -- int, option kind value

        Returns:
            * dict -- extracted IPv6_Opts option

        Structure of option type field [RFC 791]:

            Octets      Bits        Name                        Descriptions
              0           0     ipv6_opts.opt.type.value    Option Number
              0           0     ipv6_opts.opt.type.action   Action (00-11)
              0           2     ipv6_opts.opt.type.change   Change Flag (0/1)

        """
        bin_ = bin(kind)[2:].zfill(8)
        type_ = dict(
            value=kind,
            action=_IPv6_Opts_ACT.get(bin_[:2]),
            change=True if int(bin_[2], base=2) else False,
        )
        return type_

    def _read_ipv6_opts_options(self, length):
        """Read IPv6_Opts options.

        Positional arguments:
            * length -- int, length of options

        Returns:
            * dict -- extracted IPv6_Opts options

        """
        counter = 0         # length of read options
        optkind = list()    # option type list
        options = dict()    # dict of option data

        while counter < length:
            # break when eol triggered
            code = self._read_unpack(1)
            if not code:
                break

            # extract parameter
            abbr, desc = _IPv6_Opts_OPT.get(code, ('None', 'Unassigned'))
            data = _IPv6_Opts_PROC(abbr)(self, code, desc=desc)
            enum = _OPT_TYPE.get(code)

            # record parameter data
            counter += data['length']
            if enum in optkind:
                if isinstance(options[abbr], tuple):
                    options[abbr] += (Info(data),)
                else:
                    options[abbr] = (Info(options[abbr]), Info(data))
            else:
                optkind.append(enum)
                options[abbr] = data

        # check threshold
        if counter != length:
            raise ProtocolError(f'{self.alias}: invalid format')

        return tuple(optkind), options

    def _read_opt_none(self, code, *, desc):
        """Read IPv6_Opts unassigned options.

        Structure of IPv6_Opts unassigned options [RFC 8200]:
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- - - - - - - - -
            |  Option Type  |  Opt Data Len |  Option Data
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- - - - - - - - -

            Octets      Bits        Name                        Description
              0           0     ipv6_opts.opt.type          Option Type
              0           0     ipv6_opts.opt.type.value    Option Number
              0           0     ipv6_opts.opt.type.action   Action (00-11)
              0           2     ipv6_opts.opt.type.change   Change Flag (0/1)
              1           8     ipv6_opts.opt.length        Length of Option Data
              2          16     ipv6_opts.opt.data          Option Data

        """
        _type = self._read_opt_type(code)
        _size = self._read_unpack(1)
        _data = self._read_fileng(_size)

        opt = dict(
            desc=_IPv6_Opts_NULL.get(code, desc),
            type=_type,
            length=_size + 2,
            data=_data,
        )

        return opt

    def _read_opt_pad(self, code, *, desc):
        """Read IPv6_Opts padding options.

        Structure of IPv6_Opts padding options [RFC 8200]:
            * Pad1 Option:
                +-+-+-+-+-+-+-+-+
                |       0       |
                +-+-+-+-+-+-+-+-+

                Octets      Bits        Name                        Description
                  0           0     ipv6_opts.pad.type          Option Type
                  0           0     ipv6_opts.pad.type.value    Option Number
                  0           0     ipv6_opts.pad.type.action   Action (00)
                  0           2     ipv6_opts.pad.type.change   Change Flag (0)

            * PadN Option:
                +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- - - - - - - - -
                |       1       |  Opt Data Len |  Option Data
                +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+- - - - - - - - -

                Octets      Bits        Name                        Description
                  0           0     ipv6_opts.pad.type          Option Type
                  0           0     ipv6_opts.pad.type.value    Option Number
                  0           0     ipv6_opts.pad.type.action   Action (00)
                  0           2     ipv6_opts.pad.type.change   Change Flag (0)
                  1           8     ipv6_opts.opt.length        Length of Option Data
                  2          16     ipv6_opts.pad.padding       Padding

        """
        _type = self._read_opt_type(code)

        if code == 0:
            opt = dict(
                desc=desc,
                type=_type,
                length=1,
            )
        elif code == 1:
            _size = self._read_unpack(1)
            _padn = self._read_fileng(_size)

            opt = dict(
                desc=desc,
                type=_type,
                length=_size + 2,
                padding=_padn,
            )
        else:
            raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')

        return opt

    def _read_opt_tun(self, code, *, desc):
        """Read IPv6_Opts Tunnel Encapsulation Limit option.

        Structure of IPv6_Opts Tunnel Encapsulation Limit option [RFC 2473]:
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |  Next Header  |Hdr Ext Len = 0| Opt Type = 4  |Opt Data Len=1 |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            | Tun Encap Lim |PadN Opt Type=1|Opt Data Len=1 |       0       |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

            Octets      Bits        Name                        Description
              0           0     ipv6_opts.tun.type          Option Type
              0           0     ipv6_opts.tun.type.value    Option Number
              0           0     ipv6_opts.tun.type.action   Action (00)
              0           2     ipv6_opts.tun.type.change   Change Flag (0)
              1           8     ipv6_opts.tun.length        Length of Option Data
              2          16     ipv6_opts.tun.limit         Tunnel Encapsulation Limit

        """
        _type = self._read_opt_type(code)
        _size = self._read_unpack(1)
        if _size != 1:
            raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')
        _limt = self._read_unpack(1)

        opt = dict(
            desc=desc,
            type=_type,
            length=_size + 2,
            limit=_limt,
        )

        return opt

    def _read_opt_ra(self, code, *, desc):
        """Read IPv6_Opts Router Alert option.

        Structure of IPv6_Opts Router Alert option [RFC 2711]:
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |0 0 0|0 0 1 0 1|0 0 0 0 0 0 1 0|        Value (2 octets)       |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

            Octets      Bits        Name                        Description
              0           0     ipv6_opts.ra.type           Option Type
              0           0     ipv6_opts.ra.type.value     Option Number
              0           0     ipv6_opts.ra.type.action    Action (00)
              0           2     ipv6_opts.ra.type.change    Change Flag (0)
              1           8     ipv6_opts.opt.length        Length of Option Data
              2          16     ipv6_opts.ra.value          Value

        """
        _type = self._read_opt_type(code)
        _size = self._read_unpack(1)
        if _size != 2:
            raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')
        _rval = self._read_unpack(2)

        if 4 <= _rval <= 35:
            _dscp = f'Aggregated Reservation Nesting Level {_rval-4}'   # [RFC 3175]
        elif 36 <= _rval <= 67:
            _dscp = f'QoS NSLP Aggregation Level {_rval-36}'            # [RFC 5974]
        elif 65503 <= _rval <= 65534:
            _dscp = 'Reserved for experimental use'                     # [RFC 5350]
        else:
            _dscp = _ROUTER_ALERT.get(_rval, 'Unassigned')

        opt = dict(
            desc=desc,
            type=_type,
            length=_size + 2,
            value=_rval,
            alert=_dscp,
        )

        return opt

    def _read_opt_calipso(self, code, *, desc):
        """Read IPv6_Opts CALIPSO option.

        Structure of IPv6_Opts CALIPSO option [RFC 5570]:
            ------------------------------------------------------------
            | Next Header | Hdr Ext Len   | Option Type | Option Length|
            +-------------+---------------+-------------+--------------+
            |             CALIPSO Domain of Interpretation             |
            +-------------+---------------+-------------+--------------+
            | Cmpt Length |  Sens Level   |     Checksum (CRC-16)      |
            +-------------+---------------+-------------+--------------+
            |      Compartment Bitmap (Optional; variable length)      |
            +-------------+---------------+-------------+--------------+

            Octets      Bits        Name                            Description
              0           0     ipv6_opts.calipso.type          Option Type
              0           0     ipv6_opts.calipso.type.value    Option Number
              0           0     ipv6_opts.calipso.type.action   Action (00)
              0           2     ipv6_opts.calipso.type.change   Change Flag (0)
              1           8     ipv6_opts.calipso.length        Length of Option Data
              2          16     ipv6_opts.calipso.domain        CALIPSO Domain of Interpretation
              6          48     ipv6_opts.calipso.cmpt_len      Cmpt Length
              7          56     ipv6_opts.calipso.level         Sens Level
              8          64     ipv6_opts.calipso.chksum        Checksum (CRC-16)
              9          72     ipv6_opts.calipso.bitmap        Compartment Bitmap

        """
        _type = self._read_opt_type(code)
        _size = self._read_unpack(1)
        if _size < 8 and _size % 8 != 0:
            raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')
        _cmpt = self._read_unpack(4)
        _clen = self._read_unpack(1)
        if _clen % 2 != 0:
            raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')
        _sens = self._read_unpack(1)
        _csum = self._read_fileng(2)

        opt = dict(
            desc=desc,
            type=_type,
            length=_size + 2,
            domain=_cmpt,
            cmpt_len=_clen * 4,
            level=_sens,
            chksum=_csum,
        )

        if _clen:
            _bmap = list()
            for _ in range(_clen // 2):
                _bmap.append(self._read_binary(8))
            opt['bitmap'] = tuple(_bmap)

        _plen = _size - _clen * 4 - 8
        if _plen:
            self._read_fileng(_plen)

        return opt

    def _read_opt_smf_dpd(self, code, *, desc):
        """Read IPv6_Opts SMF_DPD option.

        Structure of IPv6_Opts SMF_DPD option [RFC 5570]:
            * IPv6 SMF_DPD Option Header in I-DPD mode
                 0                   1                   2                   3
                 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
                +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                               ...              |0|0|0|  01000  | Opt. Data Len |
                +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                |0|TidTy| TidLen|             TaggerId (optional) ...           |
                +-+-+-+-+-+-+-+-+               +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                |                               |            Identifier  ...
                +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

                Octets      Bits        Name                            Description
                  0           0     ipv6_opts.smf_dpd.type          Option Type
                  0           0     ipv6_opts.smf_dpd.type.value    Option Number
                  0           0     ipv6_opts.smf_dpd.type.action   Action (00)
                  0           2     ipv6_opts.smf_dpd.type.change   Change Flag (0)
                  1           8     ipv6_opts.smf_dpd.length        Length of Option Data
                  2          16     ipv6_opts.smf_dpd.dpd_type      DPD Type (0)
                  2          17     ipv6_opts.smf_dpd.tid_type      TaggerID Type
                  2          20     ipv6_opts.smf_dpd.tid_len       TaggerID Length
                  3          24     ipv6_opts.smf_dpd.tid           TaggerID
                  ?           ?     ipv6_opts.smf_dpd.id            Identifier

            * IPv6 SMF_DPD Option Header in H-DPD Mode
                 0                   1                   2                   3
                 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
                +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                               ...              |0|0|0| OptType | Opt. Data Len |
                +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                |1|    Hash Assist Value (HAV) ...
                +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

                Octets      Bits        Name                        Description
                  0           0     ipv6_opts.smf_dpd.type         Option Type
                  0           0     ipv6_opts.smf_dpd.type.value   Option Number
                  0           0     ipv6_opts.smf_dpd.type.action  Action (00)
                  0           2     ipv6_opts.smf_dpd.type.change  Change Flag (0)
                  1           8     ipv6_opts.smf_dpd.length       Length of Option Data
                  2          16     ipv6_opts.smf_dpd.dpd_type     DPD Type (1)
                  2          17     ipv6_opts.smf_dpd.hav          Hash Assist Value

        """
        _type = self._read_opt_type(code)
        _size = self._read_unpack(1)
        _tidd = self._read_binary(1)

        if _tidd[0] == '0':
            _mode = 'I-DPD'
            _tidt = _TID_TYPE.get(_tidd[1:4], 'Unassigned')
            _tidl = int(_tidd[4:], base=2)
            if _tidt == 'NULL':
                if _tidl != 0:
                    raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')
                _iden = self._read_fileng(_size-1)

                opt = dict(
                    desc=desc,
                    type=_type,
                    length=_size + 2,
                    dpd_type=_mode,
                    tid_type=_tidt,
                    tid_len=_tidl,
                    id=_iden,
                )
            elif _tidt == 'IPv4':
                if _tidl != 3:
                    raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')
                _tidf = self._read_fileng(4)
                _iden = self._read_fileng(_size-4)

                opt = dict(
                    desc=desc,
                    type=_type,
                    length=_size + 2,
                    dpd_type=_mode,
                    tid_type=_tidt,
                    tid_len=_tidl,
                    tid=ipaddress.ip_address(_tidf),
                    id=_iden,
                )
            elif _tidt == 'IPv6':
                if _tidl != 15:
                    raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')
                _tidf = self._read_fileng(15)
                _iden = self._read_fileng(_size-15)

                opt = dict(
                    desc=desc,
                    type=_type,
                    length=_size + 2,
                    dpd_type=_mode,
                    tid_type=_tidt,
                    tid_len=_tidl,
                    tid=ipaddress.ip_address(_tidf),
                    id=_iden,
                )
            else:
                _tidf = self._read_unpack(_tidl+1)
                _iden = self._read_fileng(_size-_tidl-2)

                opt = dict(
                    desc=desc,
                    type=_type,
                    length=_size + 2,
                    dpd_type=_mode,
                    tid_type=_tidt,
                    tid_len=_tidl,
                    tid=_tidf,
                    id=_iden,
                )
        elif _tidd[0] == '1':
            _data = self._read_binary(_size-1)

            opt = dict(
                desc=desc,
                type=_type,
                length=_size + 2,
                dpd_type=_mode,
                tid_type=_tidt,
                hav=_tidd[1:] + _data,
            )
        else:
            raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')

        return opt

    def _read_opt_pdm(self, code, *, desc):
        """Read IPv6_Opts PDM option.

        Structure of IPv6_Opts PDM option [RFC 8250]:
             0                   1                   2                   3
             0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |  Option Type  | Option Length |    ScaleDTLR  |     ScaleDTLS |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |   PSN This Packet             |  PSN Last Received            |
            |-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |   Delta Time Last Received    |  Delta Time Last Sent         |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

            Octets      Bits        Name                        Description
              0           0     ipv6_opts.pdm.type          Option Type
              0           0     ipv6_opts.pdm.type.value    Option Number
              0           0     ipv6_opts.pdm.type.action   Action (00)
              0           2     ipv6_opts.pdm.type.change   Change Flag (0)
              1           8     ipv6_opts.pdm.length        Length of Option Data
              2          16     ipv6_opts.pdm.scaledtlr     Scale Delta Time Last Received
              3          24     ipv6_opts.pdm.scaledtls     Scale Delta Time Last Sent
              4          32     ipv6_opts.pdm.psntp         Packet Sequence Number This Packet
              6          48     ipv6_opts.pdm.psnlr         Packet Sequence Number Last Received
              8          64     ipv6_opts.pdm.deltatlr      Delta Time Last Received
              10         80     ipv6_opts.pdm.deltatls      Delta Time Last Sent

        """
        _type = self._read_opt_type(code)
        _size = self._read_unpack(1)
        if _size != 10:
            raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')
        _stlr = self._read_unpack(1)
        _stls = self._read_unpack(1)
        _psnt = self._read_unpack(2)
        _psnl = self._read_unpack(2)
        _dtlr = self._read_unpack(2)
        _dtls = self._read_unpack(2)

        opt = dict(
            desc=desc,
            type=_type,
            length=_size + 2,
            scaledtlr=datetime.timedelta(seconds=_stlr),
            scaledtls=datetime.timedelta(seconds=_stls),
            psntp=_psnt,
            psnlr=_psnl,
            deltatlr=datetime.timedelta(seconds=_dtlr),
            deltatls=datetime.timedelta(seconds=_dtls),
        )

        return opt

    def _read_opt_qs(self, code, *, desc):
        """Read IPv6_Opts Quick Start option.

        Structure of IPv6_Opts Quick-Start option [RFC 4782]:
            * A Quick-Start Request.
                 0                   1                   2                   3
                 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
                +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                |   Option      |  Length=6     | Func. | Rate  |   QS TTL      |
                |               |               | 0000  |Request|               |
                +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                |                        QS Nonce                           | R |
                +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            * Report of Approved Rate.
                 0                   1                   2                   3
                 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
                +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                |   Option      |  Length=6     | Func. | Rate  |   Not Used    |
                |               |               | 1000  | Report|               |
                +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                |                        QS Nonce                           | R |
                +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

            Octets      Bits        Name                        Description
              0           0     ipv6_opts.qs.type           Option Type
              0           0     ipv6_opts.qs.type.value     Option Number
              0           0     ipv6_opts.qs.type.action    Action (00)
              0           2     ipv6_opts.qs.type.change    Change Flag (1)
              1           8     ipv6_opts.qs.length         Length of Option Data
              2          16     ipv6_opts.qs.func           Function (0/8)
              2          20     ipv6_opts.qs.rate           Rate Request / Report (in Kbps)
              3          24     ipv6_opts.qs.ttl            QS TTL / None
              4          32     ipv6_opts.qs.nounce         QS Nounce
              7          62     -                           Reserved

        """
        _type = self._read_opt_type(code)
        _size = self._read_unpack(1)
        if _size != 6:
            raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')

        _fcrr = self._read_binary(1)
        _func = int(_fcrr[:4], base=2)
        _rate = int(_fcrr[4:], base=2)
        _ttlv = self._read_unpack(1)
        _nonr = self._read_binary(4)
        _qsnn = int(_nonr[:30], base=2)

        if _func != 0 and _func != 8:
            raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')

        data = dict(
            type=_type,
            length=_size + 2,
            func=_QS_FUNC.get(_func),
            rate=40000 * (2 ** _rate) / 1000,
            ttl=None if _func else _rate,
            nounce=_qsnn,
        )

        return data

    def _read_opt_rpl(self, code, *, desc):
        """Read IPv6_Opts RPL option.

        Structure of IPv6_Opts RPL option [RFC 6553]:
             0                   1                   2                   3
             0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
                                            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                                            |  Option Type  |  Opt Data Len |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |O|R|F|0|0|0|0|0| RPLInstanceID |          SenderRank           |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |                         (sub-TLVs)                            |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

            Octets      Bits        Name                            Description
              0           0     ipv6_opts.rpl.type              Option Type
              0           0     ipv6_opts.rpl.type.value        Option Number
              0           0     ipv6_opts.rpl.type.action       Action (01)
              0           2     ipv6_opts.rpl.type.change       Change Flag (1)
              1           8     ipv6_opts.rpl.length            Length of Option Data
              2          16     ipv6_opts.rpl.flags             RPL Option Flags
              2          16     ipv6_opts.rpl.flags.down        Down Flag
              2          17     ipv6_opts.rpl.flags.rank_error  Rank-Error Flag
              2          18     ipv6_opts.rpl.flags.fwd_error   Forwarding-Error Flag
              3          24     ipv6_opts.rpl.id                RPLInstanceID
              4          32     ipv6_opts.rpl.rank              SenderRank
              6          48     ipv6_opts.rpl.data              Sub-TLVs

        """
        _type = self._read_opt_type(code)
        _size = self._read_unpack(1)
        if _size < 4:
            raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')
        _flag = self._read_binary(1)
        _rpld = self._read_unpack(1)
        _rank = self._read_unpack(2)

        opt = dict(
            desc=desc,
            type=_type,
            length=_size + 2,
            flags=dict(
                down=True if int(_flag[0], base=2) else False,
                rank_error=True if int(_flag[1], base=2) else False,
                fwd_error=True if int(_flag[2], base=2) else False,
            ),
            id=_rpld,
            rank=_rank,
        )

        if _size > 4:
            opt['data'] = self._read_fileng(_size-4)

        return opt

    def _read_opt_mpl(self, code, *, desc):
        """Read IPv6_Opts MPL option.

        Structure of IPv6_Opts MPL option [RFC 7731]:
             0                   1                   2                   3
             0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
                                            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                                            |  Option Type  |  Opt Data Len |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            | S |M|V|  rsv  |   sequence    |      seed-id (optional)       |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

            Octets      Bits        Name                            Description
              0           0     ipv6_opts.mpl.type              Option Type
              0           0     ipv6_opts.mpl.type.value        Option Number
              0           0     ipv6_opts.mpl.type.action       Action (01)
              0           2     ipv6_opts.mpl.type.change       Change Flag (1)
              1           8     ipv6_opts.mpl.length            Length of Option Data
              2          16     ipv6_opts.mpl.seed_len          Seed-ID Length
              2          18     ipv6_opts.mpl.flags             MPL Option Flags
              2          18     ipv6_opts.mpl.max               Maximum SEQ Flag
              2          19     ipv6_opts.mpl.verification      Verification Flag
              2          20     -                               Reserved
              3          24     ipv6_opts.mpl.seq               Sequence
              4          32     ipv6_opts.mpl.seed_id           Seed-ID

        """
        _type = self._read_opt_type(code)
        _size = self._read_unpack(1)
        if _size < 2:
            raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')

        _type = self._read_opt_type(code)
        _size = self._read_unpack(1)
        _smvr = self._read_binary(1)
        _seqn = self._read_unpack(1)

        opt = dict(
            desc=desc,
            type=_type,
            length=_size + 2,
            seed_len=_IPv6_Opts_SEED.get(int(_smvr[:2], base=2)),
            flags=dict(
                max=True if int(_smvr[2], base=2) else False,
                verification=True if int(_smvr[3], base=2) else False,
            ),
            seq=_seqn,
        )

        _kind = _smvr[:2]
        if _kind == '00':
            if _size != 2:
                raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')
        elif _kind == '01':
            if _size != 4:
                raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')
            opt['seed_id'] = self._read_unpack(2)
        elif _kind == '10':
            if _size != 10:
                raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')
            opt['seed_id'] = self._read_unpack(8)
        elif _kind == '11':
            if _size != 18:
                raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')
            opt['seed_id'] = self._read_unpack(16)
        else:
            opt['seed_id'] = self._read_unpack(_size-2)

        _plen = _size - opt['seed_len']
        if _plen:
            self._read_fileng(_plen)

        return opt

    def _read_opt_ilnp(self, code, *, desc):
        """Read IPv6_Opts ILNP Nonce option.

        Structure of IPv6_Opts ILNP Nonce option [RFC 6744]:
             0                   1                   2                   3
             0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            | Next Header   | Hdr Ext Len   |  Option Type  | Option Length |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            /                         Nonce Value                           /
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

            Octets      Bits        Name                            Description
              0           0     ipv6_opts.ilnp.type             Option Type
              0           0     ipv6_opts.ilnp.type.value       Option Number
              0           0     ipv6_opts.ilnp.type.action      Action (10)
              0           2     ipv6_opts.ilnp.type.change      Change Flag (0)
              1           8     ipv6_opts.ilnp.length           Length of Option Data
              2          16     ipv6_opts.ilnp.value            Nonce Value

        """
        _type = self._read_opt_type(code)
        _size = self._read_unpack(1)
        _nval = self._read_fileng(_size)

        opt = dict(
            desc=desc,
            type=_type,
            length=_size + 2,
            value=_nval,
        )

        return opt

    def _read_opt_lio(self, code, *, desc):
        """Read IPv6_Opts Line-Identification option.

        Structure of IPv6_Opts Line-Identification option [RFC 6788]:
             0                   1                   2                   3
             0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
                                            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                                            |  Option Type  | Option Length |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            | LineIDLen     |     Line ID...
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

            Octets      Bits        Name                            Description
              0           0     ipv6_opts.lio.type              Option Type
              0           0     ipv6_opts.lio.type.value        Option Number
              0           0     ipv6_opts.lio.type.action       Action (10)
              0           2     ipv6_opts.lio.type.change       Change Flag (0)
              1           8     ipv6_opts.lio.length            Length of Option Data
              2          16     ipv6_opts.lio.lid_len           Line ID Length
              3          24     ipv6_opts.lio.lid               Line ID

        """
        _type = self._read_opt_type(code)
        _size = self._read_unpack(1)
        _llen = self._read_unpack(1)
        _line = self._read_fileng(_llen)

        opt = dict(
            desc=desc,
            type=_type,
            length=_size + 2,
            lid_len=_llen,
            lid=_line,
        )

        _plen = _size - _llen
        if _plen:
            self._read_fileng(_plen)

        return opt

    def _read_opt_jumbo(self, code, *, desc):
        """Read IPv6_Opts Jumbo Payload option.

        Structure of IPv6_Opts Jumbo Payload option [RFC 2675]:
                                            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                                            |  Option Type  |  Opt Data Len |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |                     Jumbo Payload Length                      |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

            Octets      Bits        Name                            Description
              0           0     ipv6_opts.jumbo.type            Option Type
              0           0     ipv6_opts.jumbo.type.value      Option Number
              0           0     ipv6_opts.jumbo.type.action     Action (11)
              0           2     ipv6_opts.jumbo.type.change     Change Flag (0)
              1           8     ipv6_opts.jumbo.length          Length of Option Data
              2          16     ipv6_opts.jumbo.payload_len     Jumbo Payload Length

        """
        _type = self._read_opt_type(code)
        _size = self._read_unpack(1)
        if _size != 4:
            raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')
        _jlen = self._read_unpack(4)

        opt = dict(
            desc=desc,
            type=_type,
            length=_size + 2,
            payload_len=_jlen,
        )

        return opt

    def _read_opt_home(self, code, *, desc):
        """Read IPv6_Opts Home Address option.

        Structure of IPv6_Opts Home Address option [RFC 6275]:
             0                   1                   2                   3
             0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
                                            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                                            |  Option Type  | Option Length |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |                                                               |
            +                                                               +
            |                                                               |
            +                          Home Address                         +
            |                                                               |
            +                                                               +
            |                                                               |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

            Octets      Bits        Name                            Description
              0           0     ipv6_opts.home.type             Option Type
              0           0     ipv6_opts.home.type.value       Option Number
              0           0     ipv6_opts.home.type.action      Action (11)
              0           2     ipv6_opts.home.type.change      Change Flag (0)
              1           8     ipv6_opts.home.length           Length of Option Data
              2          16     ipv6_opts.home.ip               Home Address

        """
        _type = self._read_opt_type(code)
        _size = self._read_unpack(1)
        if _size != 16:
            raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')
        _addr = self._read_fileng(16)

        opt = dict(
            desc=desc,
            type=_type,
            length=_size + 2,
            ip=ipaddress.ip_address(_addr),
        )

        return opt

    def _read_opt_ip_dff(self, code, *, desc):
        """Read IPv6_Opts IP_DFF option.

        Structure of IPv6_Opts IP_DFF option [RFC 6971]:
                                 1                   2                   3
             0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |  Next Header  |  Hdr Ext Len  |  OptTypeDFF   | OptDataLenDFF |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |VER|D|R|0|0|0|0|        Sequence Number        |      Pad1     |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

            Octets      Bits        Name                            Description
              0           0     ipv6_opts.ip_dff.type           Option Type
              0           0     ipv6_opts.ip_dff.type.value     Option Number
              0           0     ipv6_opts.ip_dff.type.action    Action (11)
              0           2     ipv6_opts.ip_dff.type.change    Change Flag (1)
              1           8     ipv6_opts.ip_dff.length         Length of Option Data
              2          16     ipv6_opts.ip_dff.version        Version
              2          18     ipv6_opts.ip_dff.flags          Flags
              2          18     ipv6_opts.ip_dff.flags.dup      DUP Flag
              2          19     ipv6_opts.ip_dff.flags.ret      RET Flag
              2          20     -                               Reserved
              3          24     ipv6_opts.ip_dff.seq            Sequence Number

        """
        _type = self._read_opt_type(code)
        _size = self._read_unpack(1)
        if _size != 2:
            raise ProtocolError(f'{self.alias}: [Optno {code}] invalid format')
        _verf = self._read_binary(1)
        _seqn = self._read_unpack(2)

        opt = dict(
            desc=desc,
            type=_type,
            length=_size + 2,
            version=_verf[:2],
            flags=dict(
                dup=True if int(_verf[2], base=2) else False,
                ret=True if int(_verf[3], base=2) else False,
            ),
            seq=_seqn,
        )

        return opt
