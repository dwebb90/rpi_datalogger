import time
import subprocess

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import connect_and_collect as cac
import camera_func

#Setup GUI
win = tk.Tk()
win.title("Python GUI App")
ttk.Label(win, text="Test").pack()

label_text = tk.StringVar()
label_text.set("Ready to collect")

#keep track of collections during session
collect_count = 0

L = ttk.Label(win, textvariable=label_text)

image_path = '/home/pi/gui_apps/output/imgs/'
image_file = 'tmp.png'

def collectCallback():
    try:
        subprocess.run(["cp",f'{image_path}{image_file}',f'{image_path}{img_name}'])
        cac.collect(datetime, lat, lon, img_name)
        time.sleep(1) #delay needed so datetime is unique for quick succession collection
        global collect_count
        collect_count += 1
        label_text.set(f'Collected! ({collect_count})')
    except:
        label_text.set(f'Snap data before collecting.')

def set_variables():
    global datetime, lat, lon, img_name
    datetime = cac.get_datetime()
    lat, lon = cac.get_location()
    img_name = cac.get_img_name(datetime)

def snap():
    #TODO: find better way to deal with camera snap preview
    #camera_func.camera_preview() does not render on touch screen so currently storing tmp images that render to screen for preview before collection
    global image_file
    if image_file=='tmp.png':
        image_file='tmp2.png'
    else:
        image_file='tmp.png'

    camera_func.camera_snap(f'{image_path}{image_file}')
    set_variables()

    render = ImageTk.PhotoImage(Image.open(f'{image_path}{image_file}').resize((100,100), Image.ANTIALIAS))
    img.configure(image=render)
    img.image = render

load = Image.open(f'{image_path}{image_file}').resize((100,100), Image.ANTIALIAS) #rendering small enough to fit in window
render = ImageTk.PhotoImage(load)
img = tk.Label(win, image=render)
img.pack(side="right", fill="both", expand="yes")

tk.Button(win, text="Snap", command=snap).pack()
tk.Button(win, text="Collect", command=collectCallback).pack()

L.pack()
win.geometry("280x200") #render to fit on 3.5inch display
win.mainloop()
