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

def installUpdate(loc, full_filename, item):
    # split the full filename with location
    file = full_filename.split("/")
    arr_num = len(file)
    # actual filename with zip
    file_zip = file[arr_num-1]
    # remove the zip from the filename
    filename = file_zip.split(".zip")
        
    os.system(
        f"cd {config.local_base_dir};git pull;cp {full_filename} {config.local_base_dir}{loc}/{file_zip};cd {config.local_base_dir}{loc}/;unzip -o {file_zip};rm {file_zip}"
    )
    os.system(
        f"cd {config.local_base_dir};git add -A;git commit -m 'Install/Update {item} : {filename[0]}';git push origin branchUpdate"
    )
    return filename[0]

def startInterface(full_filename,plugin,theme):        
    if(plugin==True):
        loc = "/wp-content/plugins"
        filename = installUpdate(loc,full_filename,"plugin")
        # updateAwsServers()
        sg.Popup(f"{filename} has been successfully updated!")
    elif(theme==True):
        loc = "/wp-content/themes"
        filename = installUpdate(loc,full_filename,"theme")
        # updateAwsServers()
        sg.Popup(f"{filename} has been successfully updated!")
    else:
        print("Wrong Answer!")


def next_step(full_filename,plugin,theme):
    if(full_filename == ''):
        sg.Popup("Filename must not be empty")
    elif("zip" not in full_filename):
        sg.Popup("Filename must be a zip file")
    else:
        startInterface(full_filename,plugin,theme)
        