import config
import paramiko
import os


def connectSSH(host):
    try:
        cert = paramiko.RSAKey.from_private_key_file(config.keyfile)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(hostname=host, username=config.username, pkey=cert)
        print("connected!!!")
        stdin, stdout, stderr = c.exec_command("cd /var/www/hosts/ippei.com/httpdocs;git pull origin live")
        print(stdout.readlines())
        c.close()
        print("Successfully Updated")
    except:
        print("Connection Failed!!!")

def updateAwsServers():
    servers = [config.host1, config.host2]
    for server in servers:
        connectSSH(server)

def installUpdate(loc,item):
    filename = input("Name of the file?")
    base_dir = "~/Documents/Github/ippei"
    file = filename.split(".zip")
    msg = "Install/Update " + item + " - " + file[0]
    
    os.system("cd " + base_dir + ";git pull;cp ~/downloads/"+ filename + " " + base_dir + "" + loc + "/" + filename + ";cd " + base_dir + "" + loc + "/;unzip -o " + filename + ";rm " + filename + ";cd " + base_dir + ";git commit -m '" + msg + "';git push origin live")
    

process = input("[0]Plugin or [1]Theme?")

if process == "0":
    loc = "/wp-content/plugins"
    installUpdate(loc, "plugin")
    updateAwsServers()
elif process == "1":
    loc = "/wp-content/themes"
    installUpdate(loc, "theme")
    updateAwsServers()
else:
    print("Wrong Answer!")