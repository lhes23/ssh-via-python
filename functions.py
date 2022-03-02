import config
import paramiko
import os
import PySimpleGUI as sg


# Main Program
def connectSSH(host):
    try:
        cert = paramiko.RSAKey.from_private_key_file(config.keyfile)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(hostname=host, username=config.username, pkey=cert)
        print("connected!!!")
        # stdin, stdout, stderr = c.exec_command(f"cd {config.ssh_folder_location};git pull origin live")
        stdin, stdout, stderr = c.exec_command(
            f"cd {config.ssh_folder_location};git pull"
        )
        print(stdout.readlines())
        c.close()
        print("Successfully Updated")
    except:
        print("Connection Failed!!!")


def updateAwsServers():
    servers = [config.host1, config.host2]
    for server in servers:
        connectSSH(server)


def installUpdate(loc, filename, item):
    # remove the zip from the filename
    file = filename.split(".zip")
        
    os.system(
        f"cd {config.local_base_dir};git pull;cp {config.local_downloads_folder}/{filename} {config.local_base_dir}{loc}/{filename};cd {config.local_base_dir}{loc}/;unzip -o {filename};rm {filename}"
    )
    os.system(
        f"cd {config.local_base_dir};git add -A;git commit -m 'Install/Update {item} : {file[0]}';git push"
    )

def startInterface(filename,plugin,theme):        
    if(plugin==True):
        loc = "/wp-content/plugins"
        installUpdate(loc,filename,"plugin")
        updateAwsServers()
        sg.Popup(f"{filename} has been successfully updated!")
    elif(theme==True):
        loc = "/wp-content/themes"
        installUpdate(loc,filename,"theme")
        updateAwsServers()
        sg.Popup(f"{filename} has been successfully updated!")
    else:
        print("Wrong Answer!")


def next_step(filename,plugin,theme):
    if(filename == ''):
        sg.Popup("Filename must not be empty")
    elif("zip" not in filename):
        sg.Popup("Filename must be a zip file")
    else:
        startInterface(filename,plugin,theme)
        