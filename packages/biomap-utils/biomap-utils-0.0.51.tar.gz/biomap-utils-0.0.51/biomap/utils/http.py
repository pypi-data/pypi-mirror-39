import os
import requests

class HTTPSConsumer:
    def __init__(self, local_path, verbose=True):
        self.local_path = local_path
        self.verbose = verbose

    def download(self, baseurl, filename, force=False):
        local_file = os.path.join(self.local_path, filename)
        if not force and os.path.isfile(local_file):
            return local_file
        url = baseurl+'/'+filename
        if self.verbose:
            print('Downloading %s ...' % url)
        response = requests.get(url)
        if response.status_code != 200:
            print('ERROR while attempting to download %s' % url)
            return None
        with open(local_file, 'wb') as fp:
            fp.write(response.content)
        return local_file
