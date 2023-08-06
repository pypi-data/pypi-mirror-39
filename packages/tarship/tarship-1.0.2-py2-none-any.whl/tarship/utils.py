import ntpath
import os
import tarfile
import paramiko
import datetime
from scp import SCPClient


def get_instructions(source_dir):
    path = os.path.join(source_dir, 'instructions.sh')

    if not os.path.isfile(path):
        return None

    contents = ''
    with open(path) as _file:
        contents = _file.read()
    _file.close()

    return contents


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(
            source_dir,
            arcname=os.path.basename(source_dir),
            exclude=lambda x: '.git' in x or 'venv' in x or '.egg' in x
        )
    tar.close()

    return tar


def create_ssh(server, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=server, username=username, password=password)

    return ssh


def create_scp(ssh):
    return SCPClient(ssh.get_transport())


def show_output(readable):
    out = readable.read()
    if out:
        print(out)
    readable.close()


def run_deploy(source_dir, server, username, password):
    time_start = datetime.datetime.now()
    print('Starting deployment process')

    print('Gathering instructions')
    instructions = get_instructions(source_dir)
    tarname = ntpath.basename(source_dir) + '.tar.gz'

    print('Compressing: {}'.format(tarname))
    tar = make_tarfile(tarname, source_dir)

    print('Establishing ssh connection')
    ssh = create_ssh(server, username, password)

    print('Establishing scp connection')
    scp = create_scp(ssh)

    print('Sending {} to remote...'.format(tar.name))
    scp.put(tar.name, '/tmp/{}'.format(tarname))

    print('Uncompressing on remote...')
    stdin, stdout, stderr = ssh.exec_command('''
    cd /tmp; tar xzf {};
    '''.format(tarname))

    show_output(stdout)
    show_output(stderr)

    print('Executing instructions.sh on remote...')
    stdin, stdout, stderr = ssh.exec_command('cd /tmp;\n' + instructions)

    show_output(stdout)
    show_output(stderr)

    timediff = (datetime.datetime.now() - time_start)

    print('Done in {} seconds'.format(timediff.seconds))
    return tar.name
