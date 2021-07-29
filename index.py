import config
import paramiko


def connectSSH(host):
    try:
        cert = paramiko.RSAKey.from_private_key_file(config.keyfile)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("connecting...")
        c.connect(hostname=host, username=config.username, pkey=cert)
        print("connected!!!")
        stdin, stdout, stderr = c.exec_command(
            "cd /var/www/hosts/ippei.com/httpdocs;git pull origin live"
        )
        print(stdout.readlines())
        c.close()

    except:
        print("Connection Failed!!!")


servers = [config.host1, config.host2]
for server in servers:
    connectSSH(server)