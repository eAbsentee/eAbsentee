import paramiko
import os
from os import getenv
from subprocess import run
from dotenv import load_dotenv
load_dotenv(".env.prod")

host = "ssh.pythonanywhere.com"
username = getenv("PA_USER")
password = getenv("SSH_PWD")
db = getenv("PA_DB")
with paramiko.SSHClient() as ssh:
    ssh.load_system_host_keys()
    ssh.connect(host, 22, username, password)

    _, stdout, _ = ssh.exec_command(f"mysqldump -u {username} -h {username}.mysql.pythonanywhere-services.com --set-gtid-purged=OFF '{db}'", get_pty=True)

    with open("db-backup.sql", "w") as f:
        for line in stdout:
            f.write(line)
