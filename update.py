import config
import PySimpleGUI as sg
from functions import *


#GUI
font = ("Arial",20)
sg.set_options(font=font)

menu_def=['&Config', ['&Open Settings','C&lose']],['&About',['&Open Info']]

layout = [
    [sg.Menu(menu_def)],
    [sg.Text('What to Install:',font=font),sg.Radio('Plugin', "RADIO1", default=True, key="plugin", font=font),sg.Radio('Theme', "RADIO1", default=False, key='theme',font=font)],
    # [sg.Text('Filename:',font=font),sg.InputText('',key='filename',focus=True, do_not_clear=False, pad=(20,20))],
    [sg.Text("Choose a File: "),sg.Input('',key='full_filename'),sg.FileBrowse()],
    [sg.Button('Install Plugin/Theme',key='install')],
    [sg.Button("Update AWS Servers",key='update')],
    [sg.Button("Cancel")],
]
window = sg.Window(config.app_name, layout,size=(900,500),resizable=True, finalize=True)

while True:
    event,values = window.read()
    if event in (None,"Cancel", "Close"):
        break
    elif(event=='install'):
        next_step(values['full_filename'],values['plugin'],values['theme'])
    elif(event=='update'):
        updateAwsServers()
        sg.Popup("Servers has been updated!")
    elif(event=='Open Settings'):
        sg.Popup("Settings")
window.close()