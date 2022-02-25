import config
import paramiko
import os
import PySimpleGUI as sg

from tkinter import *
import tkinter as tk

from tkinter.ttk import *
from tkinter import messagebox


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


# def installUpdate(loc, item):
#     # filename = input("Name of the file?")
#     filename = filename_txt.get()
#     file = filename.split(".zip")
    
#     os.system(
#         f"cd {config.local_base_dir};git pull;cp {config.local_downloads_folder}/{filename} {config.local_base_dir}{loc}/{filename};cd {config.local_base_dir}{loc}/;unzip -o {filename};rm {filename}"
#     )
#     os.system(
#         f"cd {config.local_base_dir};git add -A;git commit -m 'Install/Update {item} : {file[0]}';git push"
#     )


def showMessage(item):
    messagebox.showinfo(
        config.app_name, f"{item} - {filename_txt.get()} has been successfully updated!"
    )

# def startInterface():
#     # process = input("[0]Plugin or [1]Theme?")
#     process = selected.get()
#     if process == 0:
#         loc = "/wp-content/plugins"
#         installUpdate(loc, "plugin")
#         updateAwsServers()
#         showMessage("Plugin")
#         filename_txt.delete(0, END)
#     elif process == 1:
#         loc = "/wp-content/themes"
#         installUpdate(loc, "theme")
#         updateAwsServers()
#         showMessage("Theme")
#         filename_txt.delete(0, END)
#     else:
#         print("Wrong Answer!")


# 17-08-2021
# updated the Personal Access Token on Github

# startInterface()
# updateAwsServers()


def next_step():
    if filename_txt.get():
        # the user entered data in the mandatory entry: proceed to next step
        startInterface()
    else:
        # the mandatory field is empty
        messagebox.showinfo(config.app_name, "Filename must not be empty!")
        filename_txt.focus_set()


def update_aws():
    updateAwsServers()
    messagebox.showinfo(config.app_name, "Servers has been updated!")


# # GUI
# window = Tk()
# window.geometry("400x200")
# window.title(config.app_name)
# window.eval("tk::PlaceWindow . center")


# thpl_lbl = Label(window, text="What to install/update?").grid(
#     column=1, row=2, pady=20, padx=20
# )
# selected = IntVar()
# plugin_rdBtn = Radiobutton(window, text="Plugin", value=0, variable=selected).grid(
#     column=2, row=2
# )
# theme_rdBtn = Radiobutton(window, text="Theme", value=1, variable=selected).grid(
#     column=3, row=2
# )

# filename_lbl = Label(window, text="File Name").grid(column=1, row=3)
# filename_txt = Entry(window, width=20)
# filename_txt.grid(column=2, row=3, columnspan=2)
# filename_txt.focus()

# submit_btn = tk.Button(
#     window, text="Update plugin/theme", command=next_step, height=2, width=20
# ).grid(column=1, columnspan=3, row=4, pady=10)
# update_server_btn = tk.Button(
#     window, text="Update AWS Server only", command=update_aws, height=2, width=20
# ).grid(column=1, row=5, columnspan=3)
# window.mainloop()


def installUpdate(loc, filename, item):
    # filename = input("Name of the file?")
    file = filename.split(".zip")
    
    sg.Popup(f"Install {item} - {filename} - {loc} \n This is the {file[0]}")
    
    # os.system(
    #     f"cd {config.local_base_dir};git pull;cp {config.local_downloads_folder}/{filename} {config.local_base_dir}{loc}/{filename};cd {config.local_base_dir}{loc}/;unzip -o {filename};rm {filename}"
    # )
    # os.system(
    #     f"cd {config.local_base_dir};git add -A;git commit -m 'Install/Update {item} : {file[0]}';git push"
    # )

def startInterface():
    # process = input("[0]Plugin or [1]Theme?")
    # process = selected.get()
    # if process == 0:
        
    #     installUpdate(loc, "plugin")
    #     updateAwsServers()
    #     showMessage("Plugin")
    #     filename_txt.delete(0, END)
    # elif process == 1:
        
    #     installUpdate(loc, "theme")
    #     updateAwsServers()
    #     showMessage("Theme")
    #     filename_txt.delete(0, END)
    # else:
    #     print("Wrong Answer!")
        
    if(values['plugin']==True):
        loc = "/wp-content/plugins"
        installUpdate(loc,values['filename'],"plugin")
        
    elif(values['themes']==True):
        loc = "/wp-content/themes"
        installUpdate(loc,values['filename'],"theme")
    else:
        print("Wrong Answer!")


#GUI
font = ("Arial",20)
sg.set_options(font=font)
layout = [
    [sg.Text('What to Install?',size=(20,1),font=font)],
    [sg.Radio('Plugin', "RADIO1", default=True, key="plugin", font=font)],
    [sg.Radio('Theme', "RADIO1", default=False, key='themes',font=font)],
    [sg.InputText('',key='filename',focus=True)],
    [sg.Button('Install Plugin/Theme',key='install')],
    [sg.Button("Update AWS Servers",key='update')],
    [sg.Button("Cancel")],
]
window = sg.Window(config.app_name, layout,size=(400,400))

while True:
    event,values = window.read()
    if event in (None,"Cancel"):
        break
    elif(event=='install'):
        if(values['filename'] == ''):
            sg.Popup("Filename must not be empty")
        elif("zip" not in values['filename']):
            sg.Popup("Filename must be a zip file")
        else:
            startInterface()
    elif(event=='update'):
        updateAwsServers()
        sg.Popup("Servers has been updated!")
window.close()