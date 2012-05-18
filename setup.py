import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
        return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name = "pygmailarchive",
        version = "0.3.0",
        author = "Andreas Pakulat",
        author_email = "apaku@gmx.de",
        description = ("An utility to archive Mails from GMail accounts."),
        license = "BSD",
        download_url = "https://github.com/downloads/apaku/pygmailarchive/pygmailarchive-0.3.0.tar.gz",
        keywords = "gmail imap archive",
        url = "https://github.com/apaku/pygmailarchive",
        install_requires = ["IMAPClient"],
        scripts = ["pygmailarchive.py"],
        data_files = [('share/doc/pygmailarchive', ['README','LICENSE'])],
        long_description = read('README'),
        classifiers = [
            "Development Status :: 3 - Alpha",
            "Topic :: Utilities",
            "Environment :: Console",
            "License :: OSI Approved :: BSD License",
        ],
)
