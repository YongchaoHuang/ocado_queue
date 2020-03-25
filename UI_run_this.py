# created by @YongchaoHuang (huangyongchao2012@gmail.com) on 24/03/2020

import subprocess
from tkinter import *
import sys
sys.path.append("/home/yongchao/PycharmProjects/pcado_queue/")

class App(Frame):
    def run_script(self):
        sys.stdout = self
        ## sys.stderr = self
        try:
            import install_packages
            import web_queue
            import test_example
        except ImportError:
            print("packages cannot be installed; pls manually install following packages on your machine:'requests','fake_headers','multiprocessing','datetime','time','logging','os','flask','threading','importlib']")
        sys.stdout = sys.__stdout__
        ## sys.stderr = __stderr__

    def stop_script(self):
        print("running stopped")
        sys.exit()
        self.quit

    def keep_calm_carry_onion(self):
        print("if u are having fun, pls do not hesitate to let me know (huangyongchao2012@gmail.com)")

    def build_widgets(self):
        self.text1 = Text(self)
        self.text1.pack(side=TOP)
        self.START = Button(self)
        self.START["text"] = "Click here to start queuing (just click once and wait, results will display in console)"
        self.START["fg"] = "blue"
        self.START["command"] = self.run_script
        self.START.pack(side=TOP)

        self.NOTHING = Button(self)
        self.NOTHING["text"] = "Do nothing but keep calm and carry onion"
        self.NOTHING["fg"] = "green"
        self.NOTHING["command"] = self.keep_calm_carry_onion
        self.NOTHING.pack({"side": "left"})


        self.QUIT = Button(self)
        self.QUIT["text"] = "quit"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.stop_script
        self.QUIT.pack({"side": "bottom"})

    def write(self, txt):
        self.text1.insert(INSERT, txt)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.build_widgets()

root = Tk()
app = App(master = root)
app.mainloop()


