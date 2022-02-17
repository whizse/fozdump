#!/usr/bin/python3

# A naive implementation to list and dump Fossilize files.
#
# It is intended to be used with, and have only been tested against,
# serialized video files used by the Steam client.
#
# Database format: https://github.com/ValveSoftware/Fossilize/blob/master/fossilize_db.cpp#L955
#
# Copyright (C) 2022  sa@whiz.se
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import struct
import argparse
import mimetypes

magic = None
try:
    import magic
except ImportError:
    pass

header_pattern = "<12sBBBB"
header_size = struct.calcsize(header_pattern)
entry_pattern = "<24s16sIIII"
entry_size = struct.calcsize(entry_pattern)

def parse_header(data):
    header_data = data.read(header_size)
    foz_magic, unused1, unused2, unused3, version = struct.unpack(header_pattern, header_data)

    if foz_magic != b'\x81FOSSILIZEDB':
        print("ERROR: Not a fossilized file.")
        exit(1)

    if version != 6:
        print("WARN: Untested version %d. Expect problems." % version)

    return data

def dump_payload(name, mime, data):
    ext = mimetypes.guess_extension(mime)
    if ext is None:
        ext = ".dat"
    with open("%s%s" % (name, ext), "wb") as out:
        out.write(data)

def parse_entry(data):
    tag, hash, stored_size, flags, crc32, payload_size = struct.unpack(entry_pattern, entry_data)
    tag = tag.decode("ascii")
    hash = hash.decode("ascii") # murmur3 hash?
    crc32 = hex(crc32)
    payload_data = foz_data.read(payload_size)
    mime = ""

    if magic:
        mime = magic.from_buffer(payload_data[:2048], mime=True)

    if args.list:
        if mime:
            print("%s\t" % mime, end="")
        print("%s\t%s\t%d\t%d\t%s\t%d" % (tag, hash, stored_size, flags, crc32, payload_size))

    if args.dump:
        dump_payload(hash, mime, payload_data)

parser = argparse.ArgumentParser(description='List and dump fossilize db files.')
parser.add_argument('filename', metavar='video.foz', help='a fossilize file')
parser.add_argument('-l', '--list', dest='list', action="store_true", help="list payload (default)")
parser.add_argument('-d', '--dump', dest='dump', action="store_true", help="dump payload")

args = parser.parse_args()

if (not args.list) and (not args.dump): # default to list  with no arguments 
    args.list = True

try:
    with open(args.filename, "rb") as foz_data:
        parse_header(foz_data)

        while True:
            entry_data = foz_data.read(entry_size)
            if entry_data == b'':
                break
            else:
                parse_entry(entry_data)
except FileNotFoundError:
    print("ERROR: File not found %s" % args.filename)
    exit(1)
