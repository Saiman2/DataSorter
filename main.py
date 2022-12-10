from tkinter import *
from tkinter import ttk
from Clients import orbico, vali
import logging
class Main(Tk):
    runOnce = True
    isInterface = False
    appRunningFlag = False

    # controller = Controller()

    def __init__(self, *args, **kwargs):
        logging.basicConfig(filename='app.log', filemode='w',
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # logging.warning('This will get logged to a file')

        self.vali = vali.Vali(logging)
        # self.orbico = orbico.Orbico()
        if self.isInterface:

            Tk.__init__(self, *args, **kwargs)
            self.geometry('500x300')
            self.title("DataSorter")
            ttk.Button(self, text='Start', command=self.start).grid(row=5, column=1, sticky=W, padx=(40, 40))
            ttk.Button(self, text='Stop', command=self.stop).grid(row=5, column=5, sticky=E, padx=(40, 40))
            self.after(8000, self.loop)



    def run(self):
        # self.orbico.run()
        self.vali.run()

    def loop(self):
        if self.appRunningFlag:
            self.run()
        self.after(8000, self.loop)

    def start(self):
        # minimizeAfterStart
        # self.wm_state('iconic')
        print('start')
        self.appRunningFlag = True

    def stop(self):
        print('stop')
        self.appRunningFlag = False

    # def interface(self):


app = Main()
if app.isInterface:
    app.mainloop()
else:
    app.run()