from argparse import ArgumentParser

parser = ArgumentParser(description='Add a new email-group relationship to the group_references table.')
parser.add_argument('email')
parser.add_argument('group_code')
args = parser.parse_args()

from paramiko import SSHClient, AutoAddPolicy
from os import getenv
from dotenv import load_dotenv
load_dotenv()

username = getenv("PA_USER")
password = getenv("SSH_PWD")

from sys import stderr

with SSHClient() as ssh:
    # ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(
        hostname="ssh.pythonanywhere.com",
        username=username,
        password=password,
    )
    _, whoami_stdout, whoami_stderr = ssh.exec_command("whoami")
    assert "".join(whoami_stdout.readlines()).strip() == username

    # TODO: use SSH forwarding in order to be able to use a Python wrapper for mysql
    count_stdin, count_stdout, count_stderr = ssh.exec_command(f"mysql -u {username} -h {username}.mysql.pythonanywhere-services.com -e 'INSERT INTO group_references(email, group_code) VALUES (\"{args.email}\", \"{args.group_code}\")' '{username}$users'")
    print("".join(count_stdout.readlines()))
    print("".join(count_stderr.readlines()), file=stderr)
    count_stdin.close()
    count_stdout.close()
    count_stderr.close()