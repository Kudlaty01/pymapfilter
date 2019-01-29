#!/usr/bin/env python3
import sys
from imaplib import IMAP4_SSL
from config import *
from ssl import SSLContext
from ssl_protocols import ssl_protocols

class PyMapFilter(object):
    """class for mail filtering based on accounts"""
    def __init__(self, account):
        """protocols initialization"""
        pass

    def filterAccount(self):
        """filter configured account by it's redirections"""
        sslC = SSLContext(ssl_protocols[account.ssl])

        self.imap_server = IMAP4_SSL(account.server, account.port, ssl_context = sslC)
        self.imap_server.login(account.login, account.password)
        try:
            self.imap_server.select()
            for target in account.redirections:
                print('moving to:\t%s' % target)
                for redir in account.redirections[target]:
                    print('processing query:\t%s' % redir)
                    typ, data = self.imap_server.search(None, redir)
                    messages = data[0].split()
                    for msg in messages:
                        self.imap_server.copy(msg, target)
                        self.imap_server.store(msg, '+FLAGS', '\\Deleted')
                        sys.stdout.write('.')
                    print('moved %d messages' % len(messages))
        except Exception as e:
            print('An error occured!')
            # raise e
        self.imap_server.close()
        self.imap_server.logout()

def main(argv):
    """main function to be executed id file run from command line"""
    print("let's process some messages!")
    pymap_filter = PyMapFilter()
    for account in accounts:
        if account.name != None:
            print("Now processing: %s" % account.name)
        pymap_filter.filterAccount(account)
    print("all done!")


if __name__ == "__main__":
    main(sys.argv[1:])
