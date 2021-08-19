import config
import paramiko
import os


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
    # filename = input("Name of the file?")
    filename = filename_txt.get()
    base_dir = "~/Documents/Github/ippei"
    file = filename.split(".zip")
    
    os.system("cd " + base_dir + ";git pull;cp ~/downloads/"+ filename + " " + base_dir + "" + loc + "/" + filename + ";cd " + base_dir + "" + loc + "/;unzip -o " + filename + ";rm " + filename)
    os.system("cd " + base_dir + ";git commit -a -m 'Install/Update " + item + " : "+file[0]+"';git push")
    
def startInterface():
    # process = input("[0]Plugin or [1]Theme?")
    process = selected.get()
    if process == 0:
        loc = "/wp-content/plugins"
        installUpdate(loc, "plugin")
        updateAwsServers()
        messagebox.showinfo('Plugin/Theme Updater','Plugin - '+ filename_txt.get() +' has been successfully updated!')
    elif process == 1:
        loc = "/wp-content/themes"
        installUpdate(loc, "theme")
        updateAwsServers()
        messagebox.showinfo('Plugin/Theme Updater','Theme - '+ filename_txt.get() +' has been successfully updated!')
    else:
        print("Wrong Answer!")

# 17-08-2021
# updated the Personal Access Token on Github

#startInterface()
#updateAwsServers()


# GUI
window = Tk()
window.geometry('350x200')
window.title("Plugin/Theme Updater/Installer")
window.eval('tk::PlaceWindow . center')

filename_lbl = Label(window,text="File Name").grid(column=1,row=2)
filename_txt = Entry(window,width=15)
filename_txt.grid(column=2,row=2)
filename_txt.focus()

selected = IntVar()

plugin_rdBtn = Radiobutton(window,text='Plugin', value=0, variable=selected).grid(column=1, row=1)

theme_rdBtn = Radiobutton(window,text='Theme', value=1, variable=selected).grid(column=2, row=1)

submit_btn = tk.Button(window, text="Submit",command=startInterface,height=2,width=20).grid(column=2, row=3)

window.mainloop()