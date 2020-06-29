from tkinter import *
from tkinter import messagebox

def ExitClass(self, variable):
    self.variable = variable
    self.iExit = messagebox.askyesno('로그인', "종료 하시겠습니까?")
    if self.iExit > 0:
        self.master.destroy()
    else:
        self.variable.focus()
        