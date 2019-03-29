#!/usr/bin/env python3
import sys, asyncio
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

    async def _process_message(self, imap_server, msg, redir, target):
        """process all messages asynchronously"""
        sys.stdout.write('.')
        try:
            if(len(redir) > 1 and any(
                all(
                    redir[1][criterion].lower() not in fetched_field.decode("utf-8").lower()
                    for fetched_field in imap_server.fetch(
                        msg,
                        '(UID BODY.PEEK[HEADER.FIELDS (%s)])' % criterion
                        )[1][0]
                    )
                for criterion in redir[1]
                )):
                return 0
        except Exception as e:
            print('error: ')
            print(e)
            return 0
        imap_server.copy(msg, target)
        imap_server.store(msg, '+FLAGS', '\\Deleted')
        return 1

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
                    processes = [self._process_message(imap_server, msg, redir, target) for msg in messages]
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    moved = loop.run_until_complete(asyncio.gather(*processes))
                    print('moved %d messages' % sum(moved))
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
