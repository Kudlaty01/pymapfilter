class MailAccount(object):
    """Mail Account data holder class"""
    def __init__(self, server, login, password, port = 993, ssl = 'tls1', redirections = None, name = None):
        """initialization of the MailAccount class
        server: the imap mail server
        login: login form email
        password: mail account password
        port: optional port (default 993)
        ssl: one of the SSL dict keys (default 'tls1')
        redirections: (a dict) where to move selected mail in format Target -> [array of conditions]
        Useful link about conditions (search criteria): http://tools.ietf.org/html/rfc3501#section-6.4.4"""
        self.server = server
        self.login = login
        self.password = password
        self.port = port
        self.ssl = ssl
        self.redirections = redirections
        self.name = name
