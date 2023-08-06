from tkinter import *
from tkinter import messagebox,Tk,Button,ttk
from .proj import get
class Main():
    def __main__(): 
        root = Tk()
        root.title("музыка вк"),root.geometry("500x2500")
        get(root)
        #root.config(cursor='top_left_arrow') # красный watch-курсор
        root.resizable(True,True)
        root.mainloop()


