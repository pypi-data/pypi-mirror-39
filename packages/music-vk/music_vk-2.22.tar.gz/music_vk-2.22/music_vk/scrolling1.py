from tkinter import *
import tkinter as Tkinter;import tkinter as tk
import tkinter.ttk as ttk
class Example(Frame):
    def __init__(self, parent):
        self.parent=parent
        self.initUI()
    def initUI(self):
        self.menu = Menu(self.parent, tearoff=0)
        self.menu.add_command(label="Beep", command=self.bell)
        self.menu.add_command(label="Exit", command=self.onExit)

        self.parent.bind("<Button-3>", self.showMenu)
        #self.parent.pack()
        
    def showMenu(self, e):
        self.menu.post(e.x_root, e.y_root)

    def onExit(self):
        self.parent.destroy()

master = Tk()
master.geometry('500x700')
master.resizable(False,False)
scrollbar = Scrollbar(master)
scrollbar.place(relx=0.65,rely=0,height=master.winfo_screenheight()-100)
listbox = Listbox(master, yscrollcommand=scrollbar.set)

for i in range(100000):
    listbox.insert(END, str(i))
listbox.place(relx=0.45,rely=0.00,width=100,height=master.winfo_screenheight()-110)#)

scrollbar.config(command=listbox.yview)
Example(master)
master.mainloop()
"""
f = Tkinter.Frame(master,width=3)
f.grid(row=2, column=0, columnspan=8, rowspan=10, pady=30, padx=30)
f.config(width=5)
tree = ttk.Treeview(f, selectmode="extended")
scbHDirSel =tk.Scrollbar(f, orient=Tkinter.HORIZONTAL, command=tree.xview)
scbVDirSel =tk.Scrollbar(f, orient=Tkinter.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scbVDirSel.set, xscrollcommand=scbHDirSel.set)           
tree["columns"] = (columnListOutput)
tree.column("#0", width=40)
tree.heading("#0", text='SrNo', anchor='w')
tree.grid(row=2, column=0, sticky=Tkinter.NSEW,in_=f, columnspan=10, rowspan=10)
scbVDirSel.grid(row=2, column=10, rowspan=10, sticky=Tkinter.NS, in_=f)
scbHDirSel.grid(row=14, column=0, rowspan=2, sticky=Tkinter.EW,in_=f)
f.rowconfigure(0, weight=1)
f.columnconfigure(0, weight=1)
master.mainloop()
"""
