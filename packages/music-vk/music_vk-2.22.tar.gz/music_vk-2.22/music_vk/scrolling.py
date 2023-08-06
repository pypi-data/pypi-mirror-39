from io import BytesIO
import tkinter as tk
from urllib.request import urlopen
from PIL import Image, ImageTk

root = tk.Tk()
url = "https://pp.userapi.com/c636816/v636816452/612f5/kPOtj5EJCb0.jpg"

u = urlopen(url)
raw_data = u.read()
u.close()

im = Image.open(BytesIO(raw_data))
image = ImageTk.PhotoImage(im)
label = tk.Label(image=image)
label.pack()
root.mainloop()
