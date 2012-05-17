#!/usr/bin/env python

"""Archive your gmail mailbox to a local directory.  Supports excluding tags,
optionally recursively and stores the mails in the same hierarchy as seen via
IMAP

Copyright (c) 2012, Andreas Pakulat <apaku@gmx.de>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

__version__ = '0.1'

import email
import email.Header
import email.Utils
import os
import sys
import time
import argparse

def log(message):
    print '[%s]: %s' % (time.strftime('%H:%M:%S'), message)

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
    )

    parser.add_argument('-v', '--version', action='version', 
        version=__version__)
    parser.add_argument('-p', '--password', dest='password', required=True,
        help='Password to log into Gmail.')
    parser.add_argument('-u', '--username', dest='username', required=True,
        help='Username to log into Gmail.')
    parser.add_argument('-x', '--exclude', action='append', dest='exclude',
        help='Exclude the given tag.')
    parser.add_argument('-X', '--exclude-recursive', action='append', dest='exclude',
        help='Exclude the given tag and recursively all tags that are sub-tags of the given one.')
    parser.add_argument('archivedir',
        help='Directory where to store the downloaded imap folders. Will also contain metadata to avoid re-downloading all files.')

    args = parser.parse_args()
    log(args)

if __name__ == '__main__':
    main()