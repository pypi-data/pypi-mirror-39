from tkinter import filedialog as fd


def extractText(name):
    file_name = fd.asksaveasfilename(initialfile=name,filetypes=(("mp3 files", "*.mp3*"),
                                                ("All files", "*.*") ))
    if ".mp3" != file_name[len(file_name)-4:len(file_name)]:
        return file_name+".mp3"
    else:
        return file_name
        
 
