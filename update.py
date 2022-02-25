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

def startInterface():        
    if(values['plugin']==True):
        loc = "/wp-content/plugins"
        installUpdate(loc,values['filename'],"plugin")
        updateAwsServers()
        sg.Popup(f"{values['filename']} has been successfully updated!")
    elif(values['themes']==True):
        loc = "/wp-content/themes"
        installUpdate(loc,values['filename'],"theme")
        updateAwsServers()
        sg.Popup(f"{values['filename']} has been successfully updated!")
    else:
        print("Wrong Answer!")

def next_step(filename):
    if(filename == ''):
        sg.Popup("Filename must not be empty")
    elif("zip" not in values['filename']):
        sg.Popup("Filename must be a zip file")
    else:
        startInterface()

#GUI
font = ("Arial",20)
sg.set_options(font=font)

menu_def=['&Config', ['&Open Settings','C&lose']],['&About',['&Open Info']]
layout = [
    [sg.Menu(menu_def)],
    [sg.Text('What to Install?',font=("Arial",30))],
    [sg.Radio('Plugin', "RADIO1", default=True, key="plugin", font=font),sg.Radio('Theme', "RADIO1", default=False, key='themes',font=font)],
    [sg.InputText('',key='filename',focus=True, do_not_clear=False, pad=(20,20))],
    [sg.Button('Install Plugin/Theme',key='install')],
    [sg.Button("Update AWS Servers",key='update')],
    [sg.Button("Cancel")],
]
window = sg.Window(config.app_name, layout,size=(400,400),element_justification='c')

while True:
    event,values = window.read()
    if event in (None,"Cancel", "Close"):
        break
    elif(event=='install'):
        next_step(values['filename'])
    elif(event=='update'):
        updateAwsServers()
        sg.Popup("Servers has been updated!")
    elif(event=='Open Settings'):
        sg.Popup("Settings")
window.close()