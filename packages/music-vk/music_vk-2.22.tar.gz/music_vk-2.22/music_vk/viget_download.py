import tkinter as tk;import base64;from io import BytesIO
from tkinter import font;import vk_api;import tkinter.ttk as ttk;from urllib.request import urlopen;from PIL import Image;from PIL import ImageTk,Image
import os
from .music_play import play as music_play;from .save_file import extractText
from .menu import main
dir_path = os.path.join(os.environ['APPDATA'], 'likes')
class IsPremium(object):
    def __init__(self):
        if not os.path.exists(dir_path):
             os.makedirs(dir_path)
        
        file_path = os.path.join(dir_path, 'your_database_file.sqlite')
        self.s = sqlite3.connect(file_path)
        self.cursor = self.s.cursor()
        self.s.commit()
    def set(self):
        self.cursor.execute("DELETE FROM IsPremium")
        self.s.commit()
        self.cursor.execute("INSERT INTO info IsPremium (1)")
        self.s.commit()
    def get(self):
        self.cursor.execute("SELECT * FROM IsPremium")
        return 1 if len(self.cursor.fetchone())>0 else  1
    
class App(object):
    def __init__(self, master, VkAudio,vk,info):
        self.player = music_play(vk)
        self.count=False;self.SortDir = True
        
        self.master = tk.Toplevel(master)
        self.master.geometry('733x450');self.master.resizable(False,False);self.master.title("Музыка {} {} (id{})".format(info["first_name"],info["last_name"],info["id"]))

        self.buttons();self.VkAudio = VkAudio
        self.dataCols = ('ID', 'артист', 'Название');self.tree = ttk.Treeview(self.master, columns=self.dataCols);self.tree.grid(row=0, column=0, sticky=tk.NSEW)

        self.tree.heading('#0', text='count', anchor='center')
        self.tree.heading('#1', text='ID', anchor='center')
        self.tree.heading('#2', text='артист', anchor='center')
        self.tree.heading('#3', text='Название', anchor='w')

        self.tree.column('#0', stretch=tk.YES,minwidth=40, width=40)
        self.tree.column('#1', stretch=tk.YES, width=170,minwidth=150)
        self.tree.column('#2', stretch=tk.YES, minwidth=50, width=250)
        self.tree.column('#3', stretch=tk.YES, minwidth=50, width=253)

        self.tree.bind("<<TreeviewSelect>>", self.OnDoubleClick)
        main(self.tree,self.master,self)
        self.scrollbar = tk.Scrollbar(self.master, command=self.tree.yview)
        self.scrollbar.place(x=714,rely=0.003,height=407)

        self.scrollbar.config();self.tree.configure(yscrollcommand=self.scrollbar.set)

        style = ttk.Style(master)
        style.configure('Treeview', rowheight=38)
        for i in range(len(self.VkAudio)-1,-1,-1):
            self.add_colun(self.VkAudio[i],i)
    def add_colun(self,i,ise):
        self.tree.insert('', 0,text=str(ise), value=("audio{}_{}".format(i["owner_id"],i["id"]),i["artist"],i["title"]                                                ))
    def OnDoubleClick(self,event):
        if not self.count:
            self.dowload_button= tk.Button(text="скачать",master=self.master,command=self.download,fg="red",font=font.Font(size=15,root = self.master))
            self.dowload_button.place(rely=0.9088,relx=0.01)
            self.listen_button= tk.Button(text="прослушать",master=self.master,command=self.listen,fg="brown",font=font.Font(size=15,root = self.master))
            self.listen_button.place(rely=0.9088,relx=0.14)
        item = self.tree.selection()
        self.count = self.tree.item(item,"text")
    def buttons(self):
        self.dowload_all_button= tk.Button(text="скачать всё аудио",master=self.master,command=self.download_all,fg="orange",font=font.Font(size=15,root = self.master))
        self.dowload_all_button.place(rely=0.9088,relx=0.39)
        self.listen_all_button= tk.Button(text="прослушать всё аудио",master=self.master,command=self.listen_all,fg="green",font=font.Font(size=15,root = self.master))
        self.listen_all_button.place(rely=0.9088,relx=0.67)
    def download_all(self):
        return "ok"
    def listen_all(self):
        return "ok"
    def download(self):
        url = self.VkAudio[int(self.count)]
        file = extractText("{} {}".format(url["artist"],url["title"]))
        self.player.download(url=url["url"],file=file)
    def listen(self):
        url = self.VkAudio[int(self.count)]
        if self.player.mixer and self.player.mixer.music.get_busy():
            self.player.stop()
        self.player.start(url["url"])
    
def get(vk,VkAudio,id=None,root=None,info=None):
    VkAudio=VkAudio.get(owner_id=id)
    app = App(root,VkAudio=VkAudio,info=info,vk=vk)
    

    #root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    root.mainloop()
    
