import config
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
key = paramiko.RSAKey.from_private_key_file(config.keyfile)
ssh.connect(
    hostname=config.host, username=config.username, look_for_keys=False, pkey=key
)
