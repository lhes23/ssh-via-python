import config
import PySimpleGUI as sg
from functions import *


#GUI
font = ("Arial",20)
sg.set_options(font=font)

menu_def=['&Config', ['&Open Settings','C&lose']],['&About',['&Open Info']]

layout = [
    [sg.Menu(menu_def)],
    [sg.Text('What to Install:',font=font,pad=(0,10)),sg.Radio('Plugin', "RADIO1", default=True, key="plugin", font=font),sg.Radio('Theme', "RADIO1", default=False, key='theme',font=font)],
    [sg.Text("Choose a File: ",pad=(0,20)),sg.InputText('',key='full_filename',size=(17,1),do_not_clear=False, pad=(20,20)),sg.FileBrowse()],
    [sg.Button('Install Plugin/Theme to Staging',key='install')],
    [sg.Button("Update AWS Servers",key='update')],
    [sg.Button("Cancel")],
]

settings_layout = [
    [sg.Text('What to Install:',font=font,pad=(0,10)),sg.Radio('Plugin', "RADIO1", default=True, key="plugin", font=font),sg.Radio('Theme', "RADIO1", default=False, key='theme',font=font)],
    [sg.Button("Update AWS Servers",key='update')],
    [sg.Button("Cancel")],
]
window = sg.Window(config.app_name, layout,size=(500,300),resizable=True, finalize=True)

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
        settings = sg.Window(config.app_name, layout=settings_layout,size=(500,500),resizable=True, finalize=True)
        while True:
            settings_event = settings.read()
            if settings_event in (None,"Cancel", "Close"):
                break
            elif settings_event == sg.WIN_CLOSED:
                break
window.close()