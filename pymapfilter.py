#!/usr/bin/env python3
import sys
from imaplib import IMAP4_SSL
from config import *
from ssl import SSLContext
from ssl_protocols import ssl_protocols

class PyMapFilter(object):
    """class for mail filtering based on accounts"""
    def __init__(self, account):
        """protocols initialization
        account: MailAccount configuration"""
        self.account = account
        pass

    def _get_imap_server(self):
        """docstring for _get_imap_server"""
        try:
            self.imap_server.check()
        except Exception as e:
            account = self.account
            sslC = SSLContext(ssl_protocols[account.ssl])
            self.imap_server = IMAP4_SSL(account.server, account.port, ssl_context = sslC)
            self.imap_server.login(account.login, account.password)
        return self.imap_server


    def filterAccount(self):
        """filter configured account by it's redirections"""
        account = self.account
        imap_server = self._get_imap_server()
        try:
            imap_server.select()
            for target in account.redirections:
                for redir in account.redirections[target]:
                    if not isinstance(redir, list):
                        redir = [redir]
                    print('processing:\t%s\t=>\t%s ' % (redir,target))
                    typ, data = imap_server.search(None, redir[0])
                    print(data)
                    messages = data[0].split()
                    for msg in messages:
                        try:
                            if(any(redir[1][criterion].lower() not in imap_server.fetch(msg, '(UID BODY.PEEK[HEADER.FIELDS (%s)])' % criterion).lower() for criterion in redir[1])):
                                continue
                        except Exception as e:
                            print('error: ')
                            print(e)
                        imap_server.copy(msg, target)
                        imap_server.store(msg, '+FLAGS', '\\Deleted')
                        sys.stdout.write('.')
                    print('moved %d messages' % len(messages))
        except Exception as e:
            print('An error occured!')
            # raise e
        imap_server.close()
        imap_server.logout()

def main(argv):
    """main function to be executed id file run from command line"""
    print("let's process some messages!")
    for account in accounts:
        pymap_filter = PyMapFilter(account)
        if account.name != None:
            print("Now processing: %s" % account.name)
        pymap_filter.filterAccount()
    print("all done!")


if __name__ == "__main__":
    main(sys.argv[1:])
