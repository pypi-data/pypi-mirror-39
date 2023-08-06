import sh
from tempfile import mkstemp


def create_remote_file(text, ip, dst):
    _, temppath = mkstemp()
    with open(temppath, 'w') as f:
        f.write(text)

    sh.scp(temppath,
           f'root@{ip}:{dst}')
