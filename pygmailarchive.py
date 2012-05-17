#!/usr/bin/env python

"""Archive your gmail mailbox to a local directory.  Supports excluding tags,
optionally recursively and stores the mails in the same hierarchy as seen via
IMAP. Messages with multiple labels will be fetched into the first folder that
is seen containing them. This means in particular that the "All Mail" folder
will not necessarily contain all messages in case the mails have other labels.
This tool will not download the Spam or Trash folders at the moment.

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

#TODO: Improve handling of mails in folders and in All Mail
#TODO: Optionally download spam and/or trash

__version__ = '0.1'

import email
import email.Header
import email.Utils
import os
import stat
import sys
import time
import argparse
import imapclient
import getpass

def log(message):
    print '[%s]: %s' % (time.strftime('%H:%M:%S'), message)

def isUserReadWritableOnly(mode):
    return bool(stat.S_IRUSR & mode) and not (
            bool(stat.S_IXUSR & mode) or
            bool(stat.S_IRGRP & mode) or
            bool(stat.S_IWGRP & mode) or
            bool(stat.S_IXGRP & mode) or
            bool(stat.S_IROTH & mode) or
            bool(stat.S_IWOTH & mode) or
            bool(stat.S_IXOTH & mode) )

def readCredentials(credentialsfile, username, password):
    if credentialsfile is not None:
        if not os.path.exists(credentialsfile):
            raise Exception("Non-existing credentials file specified: '%s'" %(credentialsfile,))
        status = os.stat(credentialsfile)
        mode = status.st_mode
        if not stat.S_ISREG(mode):
            raise Exception("Credentials filename does not point to a regular file: '%s'" %(credentialsfile,))
        if not os.access(credentialsfile, os.R_OK):
            raise Exception("Credentials file '%s' is not readable by current user" %(credentialsfile,))
        if not isUserReadWritableOnly(mode):
            raise Exception("Credentials file '%s' is readable by other users, possible security problem, aborting." %(credentialsfile,))
        lines = open(credentialsfile).readlines()
        if len(lines) != 2:
            raise Exception("Invalid credentials file '%s', needs to have 2 lines, first containing the username, second line containing the password: '%s'" %(credentialsfile, ''.join(lines)))
        username = lines[0].strip()
        password = lines[1].strip()
    if username is None:
        username = raw_input("Username: ")
    if password is None:
        password = getpass.getpass()
    return (username, password)

def connectToGMail(username, password):
    imapcon = imapclient.IMAPClient("imap.gmail.com", ssl=True)
    imapcon.login(username, password)
    log("Logged in on imap.gmail.com, capabilities: %s" %(imapcon.capabilities(),))
    return imapcon

def disconnectFromGMail(imapcon):
    log("Logging out from imap.gmail.com")
    imapcon.logout()

def setupArchiveDir(archivedir):
    if not os.path.isabs(archivedir):
        archivedir = os.path.join(os.getcwd(), archivedir)
    if not os.path.exists(archivedir):
        os.makedirs(archivedir)
    return archivedir

def archiveMails(imapcon, destination, excludes, recursiveExcludes):
    log("Archiving mails, excluding: %s, recursivly: %s" %(excludes, recursiveExcludes))
    folders = []
    for folder in imapcon.list_folders():
        if not(folder[2] in excludes or len([x for x in recursiveExcludes if folder[2].startswith(x)]) > 0):
            folders.append(folder[2])
    log("Archiving folders: %s" %(folders,))

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
    )

    parser.add_argument('-v', '--version', action='version',
        version=__version__)
    parser.add_argument('-p', '--password', dest='password',
        help='Password to log into Gmail.')
    parser.add_argument('-u', '--username', dest='username',
        help='Username to log into Gmail.')
    parser.add_argument('-c', '--credentials', dest='credentialsfile',
        help='Plain text file specifying username and password. Must contain 2 lines, first one with the username, second with the password. The file needs to be readable only by the current user')
    parser.add_argument('-x', '--exclude', action='append', dest='excludes',
        default=[], help='Exclude the given tag.')
    parser.add_argument('-X', '--exclude-recursive', action='append', dest='recursiveExcludes',
        default=[], help='Exclude the given tag and recursively all tags that are sub-tags of the given one. The tag needs to be given as full path, i.e. to exclude foo/bar/baz and foo/bar/bar you need to specify foo/bar.')
    parser.add_argument('archivedir',
        help='Directory where to store the downloaded imap folders. Will also contain metadata to avoid re-downloading all files.')

    args = parser.parse_args()

    log("Arguments: %s" %(args,))

    (username, password) = readCredentials(args.credentialsfile, args.username, args.password)

    archivedir = setupArchiveDir(args.archivedir)

    imapcon = connectToGMail(username, password)

    try:
        archiveMails(imapcon, archivedir, args.excludes, args.recursiveExcludes)
    finally:
        disconnectFromGMail(imapcon)

if __name__ == '__main__':
    main()
