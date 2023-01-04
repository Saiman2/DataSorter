from tkinter import *
from tkinter import ttk
# from datetime import datetime
import time
from datetime import timedelta
from Clients import orbico, vali, polycomp, bookpoint

import logging


class Main(Tk):
    runOnce = True
    isInterface = False
    appRunningFlag = False
    settings = {
        'vali': {
            'import': True,
        },
        'bookpoint': {
            'import': True,
        }
    }

    # controller = Controller()

    def __init__(self, *args, **kwargs):
        logging.basicConfig(filename='app.log', filemode='w',
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # self.orbico = orbico.Orbico()
        # self.polycomp = polycomp.Polycomp(logging)
        if self.isInterface:
            Tk.__init__(self, *args, **kwargs)
            self.geometry('500x300')
            self.title("DataSorter")
            ttk.Button(self, text='Start', command=self.start).grid(row=5, column=1, sticky=W, padx=(40, 40))
            ttk.Button(self, text='Stop', command=self.stop).grid(row=5, column=5, sticky=E, padx=(40, 40))
            self.after(8000, self.loop)

    def run(self):
        # self.orbico.run()
        # self.polycomp.run()
        vali_time = 0
        bookpoint_time = 0
        if self.settings['vali']['import']:
            start = time.time()
            self.vali = vali.Vali(logging)
            self.vali.run()
            end = time.time()
            hours, rem = divmod(end - start, 3600)
            minutes, seconds = divmod(rem, 60)
            vali_time = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)

        if self.settings['bookpoint']['import']:
            start = time.time()
            self.bookpoint = bookpoint.BookPoint(logging)
            self.bookpoint.run()
            end = time.time()
            hours, rem = divmod(end - start, 3600)
            minutes, seconds = divmod(rem, 60)
            bookpoint_time = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)

        print('')
        print('')
        print('')
        print('')
        print('')
        print('Vali: ' + str(vali_time))
        print('Bookpoint: ' + str(bookpoint_time))
    # ToDo for item in self.settings:
    #     print(item)

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
