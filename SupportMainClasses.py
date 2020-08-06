from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt


class Pixelcollector():
    def getXY(self):
        #print(self.imageFrame.size)
        x = len(self.imageFrame[0])
        y = len(self.imageFrame)
        x = np.arange(0, x)
        y = np.arange(0, y)
        arr = np.zeros((y.size, x.size))

        cx = self.x
        cy = self.y
        r = 10

        # The two lines below could be merged, but I stored the mask
        # for code clarity.
        mask = (x[np.newaxis, :] - cx) ** 2 + (y[:, np.newaxis] - cy) ** 2 < r ** 2

        return self.x, self.y

    def getXYRGB(self):
        #print(self.imageFrame.size)
        x = len(self.imageFrame[0])
        y = len(self.imageFrame)
        x = np.arange(0, x)
        y = np.arange(0, y)
        arr = np.zeros((y.size, x.size))

        cx = self.x
        cy = self.y
        r = 10

        # The two lines below could be merged, but I stored the mask
        # for code clarity.
        mask = (x[np.newaxis, :] - cx) ** 2 + (y[:, np.newaxis] - cy) ** 2 < r ** 2

        i = 0
        r = 0
        g = 0
        b = 0
        for value in self.imageFrame[mask]:
            r += value[0]
            g += value[1]
            b += value[2]
            i += 1

        r = int(round(r/i))
        g = int(round(g/i))
        b = int(round(b/i))
        # This plot shows that only within the circle the value is set to 123.
        #plt.figure()
        #plt.pcolormesh(x, y, arr)
        #plt.colorbar()
        #plt.show()

        return self.x, self.y, r, g, b

    def __init__(self, imageFrame):
        self.x = 1
        self.y = 1
        self.imageFrame = imageFrame


        root = Tk()
        root.geometry("1920x1080")

        #setting up a tkinter canvas with scrollbars
        frame = Frame(root, bd=2, relief=SUNKEN)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        xscroll = Scrollbar(frame, orient=HORIZONTAL)
        xscroll.grid(row=1, column=0, sticky=E+W)
        yscroll = Scrollbar(frame)
        yscroll.grid(row=0, column=1, sticky=N+S)
        canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
        canvas.grid(row=0, column=0, sticky=N+S+E+W)
        xscroll.config(command=canvas.xview)
        yscroll.config(command=canvas.yview)
        frame.pack(fill=BOTH,expand=1)

        #adding the image
        #img = ImageTk.PhotoImage(Image.open(imageFrame))
        imgu = Image.fromarray(imageFrame)
        img = ImageTk.PhotoImage(imgu)


        canvas.create_image(0,0,image=img,anchor="nw")
        canvas.config(scrollregion=canvas.bbox(ALL))

        #function to be called when mouse is clicked
        def printcoords(event):
            #outputting x and y coords to console

            self.x = int(event.x + canvas.canvasx(0))
            self.y = int(event.y + canvas.canvasy(0))
            root.destroy()
        #mouseclick event
        canvas.bind("<Button 1>",printcoords)

        root.mainloop()