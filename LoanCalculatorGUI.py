import tkinter as tk
from tkinter import ttk

class LoanRepaymentUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.mainWindow = ttk.Frame(master=self, width=250, height=100)        
        self.Exit = ttk.Button(master=self.mainWindow, text="Quit", command=self.quit)
        self.Exit.grid(row=0, column=0, sticky=tk.NW)
        self.mainWindow.grid(row=1, column=0)        

if __name__=="__main__":
   '''
   generic Tk frame for Loan Repayment GUI - WIP
   '''
   window = LoanRepaymentUI()
   style = ttk.Style(window)
   style.map("TButton", foreground=[('pressed', 'blue'), ('active', 'blue')],
                        background=[('pressed', '!disabled', 'yellow'), ('active', 'green')])
   window.mainloop()