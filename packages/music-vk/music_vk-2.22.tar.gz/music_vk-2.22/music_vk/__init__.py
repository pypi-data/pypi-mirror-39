from tkinter import messagebox,Tk,Button,ttk,font,StringVar,Entry,messagebox,ttk,Label,Canvas,BooleanVar,Checkbutton
import PIL.ImageTk as images
from PIL import Image
import sqlite3,os,threading,tkinter_gif,vk_api
from wget import download
from threading import Thread
dir_path = os.path.join(os.environ['APPDATA'], 'likes')

from .init import __main2__
class dd(object):
    def __init__(self):
        
        
        if not os.path.exists(dir_path):
             os.makedirs(dir_path)
        
        file_path = os.path.join(dir_path, 'your_database_file.sqlite')
        self.s = sqlite3.connect(file_path)
        self.cursor = self.s.cursor()
        try:
            self.cursor.execute("""CREATE TABLE info (log,pass)""")
        except:
            "ok"
        self.s.commit()
    def add(self,login,password):
        self.cursor.execute("DELETE FROM info")
        self.s.commit()
        self.cursor.execute("INSERT INTO info VALUES (\""+login+"\",\""+password+"\")")
        self.s.commit()
    def get(self):
        self.cursor.execute("SELECT * FROM info")
        return self.cursor.fetchone()
    
db = dd()
def files():
    if not os.path.exists(os.path.join(dir_path, 'load.gif')):
        download("https://media.giphy.com/media/QyOI0WGW3vY2s/source.gif",out=os.path.join(dir_path, 'load.gif'))
    if not os.path.exists(os.path.join(dir_path, 'icon.ico')):
        download("https://vk.com/doc302808715_484631566",out=os.path.join(dir_path,"icon.ico"))
files()
class __main__(object):
    def __init__(self,root):
        self.root,self.mask = root, BooleanVar()
        self.font_log,self.font_vihod,self.font_normal =font.Font(size=13,root = self.root), font.Font(size=15,root = self.root),font.Font(size=25,root = self.root)

        self.buttons(),self.inputs(),self.text(),self.mask.set(False),self.check_buttons()
        #self.lines()
    def inputs(self,n=None):
        log,pas = StringVar(),StringVar()
        info = db.get()
        if not n:
            Entry(self.root, textvariable=log,font=self.font_log).place(height = 30,width=150,relx=.6, rely=.1, anchor="c")
            if info:
                log.set(info[0])
            else:
                log.set("Логин")
            self.login = log
        
        self.entry = Entry(self.root,show=["*" if not self.mask.get() else None][0], textvariable=pas,font=self.font_log)
        self.entry.place(height = 30,width=150,relx=.6, rely=.3, anchor="c")
        if info:
            pas.set(info[1] if not n else self.password.get())
        else:
            pas.set("пароль" if not n else self.password.get())
        self.password = pas
    """
    def lines(self):
        canvas = Canvas(self.root)
        s = canvas.create_line(100, 100, 100, 100)

        canvas.pack(expand=0)
    """
        
    def text(self):
        s = Label(self.root,text="Логин:",font=self.font_normal)
        s.place(height = 30,width=150,relx=.2, rely=.1, anchor="c")
        
        s = Label(self.root,text="Пароль:",font=self.font_normal)
        s.place(height = 40,width=150,relx=.2, rely=.3, anchor="c")
    def buttons(self):
        s = Button(text="Авторизоваться",command=self.auth_button,font=self.font_normal,fg="brown")
        s.config(cursor='question_arrow'),s.place(relx=.5, rely=.6, anchor="c")
        #кнопка выхода
        s1 = Button(text="выход",command=self.root.destroy,fg="red",height = 1,width = 6,font=self.font_vihod,relief="ridge")#sunken, raised,groove , and ")
        s1.bind("<Button-1>")
        s1.config(cursor='X_cursor')
        s1.place(x=300,y=230)

    def auth_button(self):
        #s = tkinter_gif.h
        #def n():
        #    s(os.path.join(dir_path, 'load.gif'))
        #sk = Thread(None,target=n)
        #sk.start()
        log,passw = self.login.get(),self.password.get()
        if not log or not passw:
            messagebox.showerror("Ошибка","Какое-то поле пустое!")
        vk = vk_api.VkApi(login=log,password=passw)                   
        try:
            vk.auth()
            q = True
        except vk_api.exceptions.BadPassword:
            q = False        
        
        if q: 
            self.root.destroy()
            db.add(log,passw)
            __main2__(vk,os.path.join(dir_path,"icon.ico"))
        else:
            messagebox.showerror("Ошибка","Неправильный логин или пароль!!!")
    def check_buttons(self):
        cb = Checkbutton(self.root, text="Показать", command=self.onClickCkeckButton)
        cb.place(height = 40,relx=.9, rely=.3, anchor="c")
    def onClickCkeckButton(self):
        q = self.mask.get();self.mask.set(True if not q else False)
        self.inputs(n="ok")
def start():
    root = Tk()
    s = Entry(root)    
    __main__(root)
    root.bindtags,root.title("музыка вк авторизация"),root.geometry("400x300"),root.config(cursor='top_left_arrow'),root.resizable(False,False),root.iconbitmap(os.path.join(dir_path,"icon.ico"))
    root.mainloop()
    
    

start()


db.s.close()
