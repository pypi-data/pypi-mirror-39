#!/usr/bin/python
# -*- coding: utf-8 -*-
from clipboard import copy
from tkinter import Tk, Frame, Menu, Button,messagebox
from .music_play import play as music_play;from .save_file import extractText

class Example(Frame):
    def __init__(self, parent,obj,selfa):
        Frame.__init__(self, parent)   
        self.parent = parent;
        self.on = selfa
        self.initUI(obj)
        
    def initUI(self,obj):
        self.menu = Menu(obj,tearoff=0);fileMenu = Menu(self.menu,tearoff=0)       
        self.menu.add_command(label="Воспроизвести", underline=0,command=self.start_play)
        self.menu.add_command(label="Скачать", underline=0,command=self.download )
        self.menu.add_cascade(label="Скопировать", underline=0, menu=fileMenu)
        
        fileMenu.add_command(label='Ссылку на аудио', underline=0, command=self.onUrl)
        fileMenu.add_command(label='ID', underline=0)

        fileMenu.add_command(label="Артист", underline=0, command=self.onArtist)

        fileMenu.add_command(label="Название", underline=0, command=self.onName)
                
        obj.bind("<Button-3>", self.showMenu)
    def start_play(self):
        self.on.listen()
    def download(self):
        self.on.download()
    def onName(self):
        return "ok"
    def onUrl(self):
        return "ok"
    def onArtist(self):
        return "ok"
    def showMenu(self, e):
        self.menu.post(e.x_root, e.y_root)
 
    def onExit(self):
        self.quit()
 
def main(button,root,self):
    app = Example(root,button,self)
 
if __name__ == '__main__':
    root = Tk()
    button = Button(text="dsaOKDSkocdS",master=root)
    button.place(relx=0.37,rely=.45)
    button1 = Button(text="dsjnj",master=root)
    button1.place(relx=0.1,rely=.1)
    root.geometry("250x150+300+300")
    
    main(button,root)
    main(button1,root)
    root.mainloop()  
