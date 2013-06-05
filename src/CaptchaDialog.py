import Image
import ImageTk
import tkinter as tk

from tempfile import NamedTemporaryFile
from urllib import request

CAPTCHA_URL = 'http://www.titulky.com/captcha/captcha.php'
#MAX_CAPTCHA_LEN = 8

root = tk.Tk()
root.title("Re-type captcha code")

mainframe = tk.Frame(root)
mainframe.grid(column=0, row=0)
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

tmp = NamedTemporaryFile(mode='w+b', prefix='captcha_', suffix='.gif')

def end():
    mainframe.destroy()
    root.destroy()


def getCaptchaCode():
    fd = request.urlopen(CAPTCHA_URL)

    tmp.write(fd.read())
    tmp.flush()

    oimg = Image.open(tmp.name)
    pimg = ImageTk.PhotoImage(oimg)

    lbl = tk.Label(mainframe, image=pimg)
    lbl.pack()

    entryCont = tk.StringVar()
    entry = tk.Entry(mainframe, textvariable=entryCont)
    entry.pack()

    confirmButton = tk.Button(mainframe, text='Confirm code', command=end)
    confirmButton.pack()

    root.mainloop()

    return entryCont.get()


print("captcha: %s" % getCaptchaCode())


