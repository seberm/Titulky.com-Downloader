import tkinter as tk
root = tk.Tk()
root.title("zk")

mainframe = tk.Frame(root)
mainframe.grid(column=0, row=0)
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

from urllib import request
url = "http://www.titulky.com/captcha/captcha.php"
fd = request.urlopen(url)

import tempfile
tmp = tempfile.TemporaryFile(mode='w+b', prefix='captcha_')
tmp.write(fd.read())

oimg = 
pimg = tk.PhotoImage(oimg)

lbl = tk.Label(mainframe, image=pimg)
#lbl = tk.Label(mainframe, text="ahoj")

# show it
lbl.pack()

root.mainloop()


# garbage
tmp.close()
