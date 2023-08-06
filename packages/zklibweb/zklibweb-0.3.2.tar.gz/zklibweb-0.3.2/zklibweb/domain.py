class Maquine:
    """
    Instance for zklib maquine
    """

    def __init__(self, host, username, password):
        """
        Create a new instance for a Mauine

        Arguments:
            host {string} -- Host
            username {string} -- username
            password {string} -- password
        """

        self._host = host
        self.username = username
        self.password = password

    def get_host(self):
        """Return the base host"""
        return 'http://{}'.format(self._host)

    def get_url_for_uids(self):
        """Get the url for get uid for al the people"""
        return 'http://{}/csl/download?first=0&last=10000'.format(self._host)

    def get_url_for_download(self):
        """Get the download url"""
        return 'http://{}/form/Download'.format(self._host)
