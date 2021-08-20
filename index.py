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

def next_step():
    if filename_txt.get():
        # the user entered data in the mandatory entry: proceed to next step
        startInterface()
    else:
        # the mandatory field is empty
        messagebox.showinfo('Plugin/Theme Updater','Filename must not be empty!')
        filename_txt.focus_set()


# GUI
window = Tk()
window.geometry('350x200')
window.title("Plugin/Theme Updater/Installer")
window.eval('tk::PlaceWindow . center')

selected = IntVar()

thpl_lbl = Label(window, text="What to install/update?").grid(column=1,row=2,pady=20,padx=20)
plugin_rdBtn = Radiobutton(window,text='Plugin', value=0, variable=selected).grid(column=2, row=2)
theme_rdBtn = Radiobutton(window,text='Theme', value=1, variable=selected).grid(column=3, row=2)

filename_lbl = Label(window,text="File Name").grid(column=1,row=3)
filename_txt = Entry(window,width=20)
filename_txt.grid(column=2,row=3, columnspan=2)
filename_txt.focus()

submit_btn = tk.Button(window, text="Submit",command=next_step,height=2,width=20).grid(column=1,columnspan=3, row=4,pady=10)

window.mainloop()
