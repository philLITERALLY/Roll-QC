# import packages
# check RAM usage // free -m -s 0.1 //
import sys
import time
from datetime import datetime
from collections import Counter

# import the GUI packages
import tkinter as tk
import threading
from PIL import Image
from PIL import ImageTk

# import my classes
import config
import settings_window

class App(threading.Thread) :
        def __init__(self) :
                threading.Thread.__init__(self)
                self.start()
        def settings_menu(self, other) :
                window = settings_window.main(self.root)
        def upCrop(self) :
                if config.cropHeightStart + config.cropHeight >= config.camHeight :
                        self.root.cropUpBtn.configure(text="MAX")
                else :
                        config.cropHeightStart += 10
                        config.cropHeightEnd = config.cropHeightStart + config.cropHeight

                if config.cropHeightStart != 0 :
                        self.root.cropDownBtn.configure(text=u"\u2B07")
        def downCrop(self) :
                if config.cropHeightStart - 10 <= 0 :
                        self.root.cropDownBtn.configure(text="MAX")
                else :
                        config.cropHeightStart -= 10
                        config.cropHeightEnd = config.cropHeightStart + config.cropHeight

                if config.cropHeightStart + config.cropHeight != config.camHeight :
                        self.root.cropUpBtn.configure(text=u"\u2B06")
        def read(self) :
                global readMode
                if (self.root.runBtn.cget('text') == "RUN") :
                        # Set App to read mode
                        readMode = True

                        # Change runBtn to stop colour
                        self.root.runBtn.configure(
                                bg="red",
                                activebackground="red",
                                text="PAUSE"
                        )

                elif (self.root.runBtn.cget('text') == "PAUSE") :
                        # Take App out of read mode
                        readMode = False

                        # Change runBtn to default
                        self.root.runBtn.configure(
                                bg="green",
                                activebackground="green",
                                text="RUN"
                        )
        def make_label(self, x, y, h, w, *args, **kwargs):
                f = tk.Frame(self.root, height=h, width=w)
                f.pack_propagate(0) # don't shrink
                f.place(x=x, y=y)
                label = tk.Label(f, *args, **kwargs)
                label.pack(fill=tk.BOTH, expand=1)
                return label
        def make_button(self, x, y, h, w, *args, **kwargs):
                f = tk.Frame(self.root, height=h, width=w)
                f.pack_propagate(0) # don't shrink
                f.place(x=x, y=y)
                button = tk.Button(f, *args, **kwargs)
                button.pack(fill=tk.BOTH, expand=1)
                return button
        def run(self) :
                self.root = tk.Tk()
                self.root.attributes("-fullscreen", True)
                self.root.updateConfig = False
                self.root.shutDown = False

                # Screen size and pixel ratios
                config.screenWidth = self.root.winfo_screenwidth()
                config.screenHeight = self.root.winfo_screenheight()
                pixelRatioWidth = 1 / config.screenWidth
                pixelRatioHeight = 1 / config.screenHeight

                # 2x2 Images Setup
                totalMargins = config.imageMargins * 4
                imageWidth = int((config.screenWidth - totalMargins) / 2)
                lblHeight = config.headerText + (config.imageMargins * 2)
                btnHeight = config.headerText + (config.imageMargins * 12)
                imageHeight = int((config.screenHeight - lblHeight - (config.imageMargins * 3) - btnHeight) / 2)
                labelHeight = config.headerText + (config.imageMargins * 2)

                # Header Setup
                headerY = config.imageMargins + imageHeight
                self.root.headerLbl = self.make_label(
                        0,
                        headerY,
                        lblHeight,
                        config.screenWidth,
                        text='LOW COST AUTOMATION',
                        font="Helvetica " + str(config.headerText) + " bold"
                )
                self.root.headerLbl.bind("<Button-1>", self.settings_menu)

                # image setup
                image = Image.open("./initialising.png").resize((imageWidth, imageHeight))
                xLeftCamera = pixelRatioWidth * config.imageMargins
                xRightCamera = pixelRatioWidth * (config.imageMargins * 2 + imageWidth)
                yTopCamera = pixelRatioHeight * config.imageMargins
                yBottomCamera = pixelRatioHeight * (imageHeight + config.imageMargins + labelHeight)

                cameraScreen1 = ImageTk.PhotoImage(image)
                self.root.cameraLabel1 = tk.Label(image=cameraScreen1)
                self.root.cameraLabel1.place(relx=xLeftCamera, rely=yTopCamera)

                cameraScreen2 = ImageTk.PhotoImage(image)
                self.root.cameraLabel2 = tk.Label(image=cameraScreen2)
                self.root.cameraLabel2.place(relx=xRightCamera, rely=yTopCamera)

                cameraScreen3 = ImageTk.PhotoImage(image)
                self.root.cameraLabel3 = tk.Label(image=cameraScreen3)
                self.root.cameraLabel3.place(relx=xLeftCamera, rely=yBottomCamera)

                cameraScreen4 = ImageTk.PhotoImage(image)
                self.root.cameraLabel4 = tk.Label(image=cameraScreen4)
                self.root.cameraLabel4.place(relx=xRightCamera, rely=yBottomCamera)

                # Run Button Setup
                runY = config.screenHeight - btnHeight - config.imageMargins
                self.root.runBtn = self.make_button(
                        config.imageMargins,
                        runY,
                        btnHeight,
                        config.screenWidth - (config.imageMargins * 2),
                        text='RUN',
                        font="Helvetica " + str(config.headerText) + " bold",
                        command=self.read,
                        bg="green",
                        activebackground="green"
                )

                self.root.title("LOW COST AUTOMATION")
                self.root.mainloop()

app = App()

# try/except statement is a pretty ugly hack to get around
# a RunTime error that Tkinter throws due to threading
while True:
        try:
                if hasattr(app, 'root') and hasattr(app.root, 'shutDown') and app.root.shutDown:
                        try:
                                app.root.quit()
                                sys.exit()
                        except Exception as ex:
                                print('Shutdown error')
                                print(ex)

        except Exception as e:
                print('Caught an error')
                print(e)