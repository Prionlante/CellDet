import tkinter as tk
import os
from filemngr import fmaneger
from imganalys import imgProcess
from tkinter import *
from datetime import datetime

MAXLENPATH = 58
IMGH = 414
IMGW = 550
BGMAIN = '#42454D'
BGACT = '#36393F'
BGCHOSE = '#7F838E'

fm = fmaneger()
improcs =imgProcess()

def opendir():
    fm.opendir()

    if len(fm.MAINPATH) <= MAXLENPATH :
        pathlb['text'] = fm.MAINPATH
    else:
        point = 0
        ind = len(fm.MAINPATH)-1
        while point < 2 :
            ind -= 1
            if(fm.MAINPATH[ind] == '/'): point += 1

        pathlb['text'] = fm.MAINPATH[0:3]+'...'+fm.MAINPATH[ind:]
    filebox.delete(0,END)

    for item in fm.FILELIST:
        pad = '      '
        text = f"{round((os.stat(fm.MAINPATH + '/' + item).st_size/(1024*1024)), 2):.{2}f} MB"
        text += pad
        text += str(datetime.fromtimestamp(os.stat(fm.MAINPATH + '/' + item).st_mtime).strftime("%d.%m.%Y"))
        text += pad
        text += "        ○     "+item
        filebox.insert(tk.END, "  " + text)

def openfile(event):
    index = int(event.widget.curselection()[0])
    fm.openimg(fm.FILELIST[index])
    img, imginfo, imgout = improcs.imanalys(imginput = fm.IMG,
                           canvassize=(IMGW, IMGH))
    imagebox.create_image(0, 0, image=img, anchor=NW)
    imagebox.image = img

    fm.getimgporc(imgout, imginfo)

    filenamelb["text"] = fm.FILELIST[index]
    Vimgbadlb["text"] = imginfo[0]
    Vimggoodlb["text"] = imginfo[1]
    Vimgsizelb['text'] = imginfo[2]
    Vimgdatelb['text'] = imginfo[3]

def openConsider():
    fm.consider()

def save():
    fm.save()

gui = tk.Tk()
gui.title('CellDet')
gui.geometry("1130x600")
gui.config(bg='#42454D')
gui.iconbitmap('resources\\CellDet.ico')
gui.resizable(False, False)

worframe = tk.Frame(master=gui, bg=BGMAIN)

# File - Show, Open, Saving
fileframe = tk.Frame(master=worframe, bg=BGMAIN)
pathlb = tk.Label(fileframe, text = "Please open image folder", font=("Arial", 14),
                  fg='#bcc0cb', bg=BGACT, height=1, width=49,
                  highlightthickness=0,
                  #highlightbackground='#bcc0cb'
                  )
pathlb.grid(row = 0, column=0, sticky='ew', pady = 5)

scrollbar = tk.Scrollbar(fileframe, orient="vertical")
filebox =tk.Listbox(fileframe, bg='#36393F', font=("Arial", 14), fg='#bcc0cb',
                    selectbackground = BGCHOSE, yscrollcommand=scrollbar.set,
                    activestyle = 'none', width = 50, height=24,
                    borderwidth=0,
                    highlightthickness=0,
                    #highlightbackground = '#bcc0cb'
                    )
filebox.bind('<Double-Button>', openfile)
filebox.grid(row = 1, column=0)
fileframe.grid(row = 0, column=0)


# Images - Show, ditails

imageframe = tk.Frame(master=worframe, bg=BGMAIN)
filenamelb = tk.Label(imageframe, text = "image", font=("Arial", 14),
                  fg='#bcc0cb', bg=BGACT, height=1, width=49,
                  highlightthickness=0,
                  #highlightbackground='#bcc0cb'
                    )
filenamelb.grid(row = 0, column=0, sticky='ew', pady = 5)
_borderframe = tk.Frame(master=imageframe,
                        highlightthickness=0,
                        #highlightbackground = '#bcc0cb'
                        )
imagebox = tk.Canvas(_borderframe, width = IMGW, height = IMGH,
                     highlightthickness = 0, relief='ridge')
imagebox.pack()
_borderframe.grid(row = 1, column=0, pady=5, sticky = 'E')

imageframe_info = tk.Frame(master=imageframe, width = IMGW, bg=BGACT,
                           highlightthickness=0,
                           #highlightbackground='#bcc0cb'
                           )
imageframe_info.grid(row = 2, column=0, sticky='we')


imgsizelb = tk.Label(imageframe_info, text='Output Size', font=("Arial", 14), bg=BGACT, fg='#bcc0cb', justify=LEFT)
Vimgsizelb = tk.Label(imageframe_info, text='1920x1080', font=("Arial", 14), bg=BGACT, fg='#bcc0cb', width=9)
imgbadlb = tk.Label(imageframe_info, text='Bad num', font=("Arial", 14), bg=BGACT, fg='#bcc0cb')
Vimgbadlb = tk.Label(imageframe_info, text='0', font=("Arial", 14), bg=BGACT, fg='#bcc0cb', width=3)
imggoodlb = tk.Label(imageframe_info, text='Good num', font=("Arial", 14), bg=BGACT, fg='#bcc0cb')
Vimggoodlb = tk.Label(imageframe_info, text='0', font=("Arial", 14), bg=BGACT, fg='#bcc0cb', width=3)
imgdatelb = tk.Label(imageframe_info, text='Time', font=("Arial", 14), bg=BGACT, fg='#bcc0cb')
Vimgdatelb = tk.Label(imageframe_info, text='22.09.12 12:35', font=("Arial", 14), bg=BGACT, fg='#bcc0cb', width=14)
_wlb = tk.Label(imageframe_info, text='                 ', font=("Arial", 14), bg=BGACT, fg='#bcc0cb')

imgbadlb.grid(row = 0, column=0, pady=5, padx = 5, sticky = W)
Vimgbadlb.grid(row = 0, column=1, pady=5, padx = 5, sticky = W)
imggoodlb.grid(row = 1, column=0, pady=5, padx = 5, sticky = W)
Vimggoodlb.grid(row = 1, column=1, pady=5, padx = 5, sticky = W)
_wlb.grid(row = 0, column=2, pady=5, padx = 5, sticky = W)
imgsizelb.grid(row = 0, column=3, pady=5, padx = 5, sticky = W)
Vimgsizelb.grid(row = 0, column=4, pady=5, padx = 5, sticky = W)
imgdatelb.grid(row = 1, column=3, pady=5, padx = 5, sticky = W)
Vimgdatelb.grid(row = 1, column=4, pady=5, sticky = W)

fileframe_buttons = tk.Frame(imageframe, bg='#42454D')
btnOpenFldr = tk.Button(fileframe_buttons, text = 'Open folder',
                        width = 12, height=1, bg ='#323232',
                        fg='#d9d9d9', font=("Arial", 14),
                        activebackground=BGCHOSE,
                        command = opendir,
                        highlightthickness=0,
                        bd = 0)
btnSave = tk.Button(fileframe_buttons, text = 'Save',
                        width = 12, height=1, bg ='#323232',
                        fg='#d9d9d9', font=("Arial", 14),
                        activebackground=BGCHOSE,
                        highlightthickness=0,
                        bd = 0, command = save)
btnCon = tk.Button(fileframe_buttons, text = 'Consider',
                        width = 12, height=1, bg ='#323232',
                        fg='#d9d9d9',font=("Arial", 14),
                        activebackground=BGCHOSE,
                        highlightthickness=0,
                        bd = 0, command = openConsider )

btnOpenFldr.grid(row = 0, column=0, pady = 10, padx = 10)
btnSave.grid(row = 0, column=1, pady = 10, padx = 10)
btnCon.grid(row = 0, column=2, pady = 10, padx = 10)

fileframe_buttons.grid(row = 3, column=0)
imageframe.grid(row = 0, column=1, padx=10)

worframe.pack()

gui.mainloop()
