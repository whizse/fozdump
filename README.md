# fozdump
A naive implementation to list and dump Fossilize files

    usage: fozdump.py [-h] [-l] [-d] video.foz

    List and dump fossilize db files.

    positional arguments:
      video.foz   a fossilize file

    optional arguments:
      -h, --help  show this help message and exit
      -l, --list  list payload (default)
      -d, --dump  dump payload

It is intended to be used with, and have only been tested against, serialized video files used by the Steam client.

The list option provides tab separated output of the following fields:
mime type, hash. tag. compressed payload size. flags, crc32 checksum, uncompressed payload size

python3-magic is used as an optional dependency to guess mime type and proper file extension for dumped payload data.
