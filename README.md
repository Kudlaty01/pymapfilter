# pymapfilter
Python-powered substitution for common mail services filtering features (often limited).
Created out of frustration with no luck in SSL/TLS connecting to one of mail servers with a popular lua utility.
Now it works asynchronously.

## Requirements
- python3
- imaplib, ssl python library

## Installation/Setup
At the moment it's not a standalone python package. Just rename `config.py.example` to `config.py` and modify it with valid data. \
It is highly recommended to use a secure password storing method (i.e. via a keyring) \
Redirections are defined by `target: [search_condition1, search_condition2 …]` \
Added possibility to further filter the search result set by matching specific fields (if imap server acts unsupportive)\
Search criteria documentation: http://tools.ietf.org/html/rfc3501#section-6.4.4

## Usage
Just run `python3 pymapfilter.py` (or `./pymapfilter.py` if chmodded to executable). 

## TODO
- create a Python package
- allow to choose verbosity level
- add remote mail searching feature
- make a class building the search criteria
