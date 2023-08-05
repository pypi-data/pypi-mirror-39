import os
import ftplib

class FTPConsumer:

    def __init__(self, ftp_server, local_root, verbose=True):
        self.ftp_server = ftp_server
        self.local_root = local_root
        self.verbose = verbose

    def download(self, path_relative_to_root, filename, force_download=True, **kwargs):

        def RETR(path):
            return 'RETR ' + path

        local_path = os.path.join(self.local_root, path_relative_to_root)
        if not os.path.isdir(local_path):
            os.makedirs(local_path)
        local_file = os.path.join(local_path, filename)
        if not force_download and os.path.isfile(local_file):
            if self.verbose:
                print('Local file {} already exists.'.format(local_file))
            return local_file
        ftp_file = path_relative_to_root+'/'+filename

        if self.verbose:
            print('\nDownloading {} to {}\n\n'.format(ftp_file, local_file))

        try:
            ftp = ftplib.FTP(self.ftp_server)
            ftp.login(**kwargs)
            ftp.retrbinary(RETR(ftp_file),
                           open(local_file, 'wb').write)
        except:
            print('FTP ERROR.')

        return local_file
