import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from datetime import date
import LoanCalculator

class LoanRepaymentUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.mainWindow = ttk.Frame(master=self, width=250, height=100)        
        
        #INPUT String Vars
        self.BegPrin = tk.StringVar(master=self, value="12000.00")
        self.StartDate = tk.StringVar(master=self, value="2022-01-15")
        self.EndDate = tk.StringVar(master=self, value="2024-1-30")
        self.BaseRate = tk.StringVar(master=self, value=".0599")
        self.PaymentAmount = tk.StringVar(master=self, value="1250.00")
        self.FrequencyKeys=list(LoanCalculator.FREQUENCY_LOOKUP.keys())
        self.Frequency = tk.StringVar(master=self, value=self.FrequencyKeys[0])
        
        #Buttons
        self.Exit = ttk.Button(master=self.mainWindow, text="Quit", command=self.quit)
        self.Exit.grid(row=0, column=0, sticky=tk.NW, padx=1, pady=4)
        self.Calculate = ttk.Button(master=self.mainWindow, text="Calculate", command=self.calculate)
        self.Calculate.grid(row=0, column=1, sticky=tk.NW, padx=1, pady=4)
        self.SaveResults = ttk.Button(master=self.mainWindow, text="Save", command=self.saveResults)
        self.SaveResults.grid(row=0, column=2, sticky=tk.NW, padx=1, pady=4)

        #Controls
        self.mainWindow.grid(row=1, column=0)        
        self.frameInputs = ttk.Frame(master=self.mainWindow)
        self.StartDateLabel = ttk.Label(master=self.frameInputs,text="Start Date")
        self.StartDateEntry = ttk.Entry(master=self.frameInputs,textvariable=self.StartDate)        
        self.EndDateLabel = ttk.Label(master=self.frameInputs,text="End Date")
        self.EndDateEntry = ttk.Entry(master=self.frameInputs,textvariable=self.EndDate)        
        self.BegPrinLabel = ttk.Label(master=self.frameInputs, text="Beginning Prin")
        self.BegPrinEntry = ttk.Entry(master=self.frameInputs,textvariable=self.BegPrin)        
        self.BaseRateLabel = ttk.Label(master=self.frameInputs,text="Annual Interest Rate")
        self.BaseRateEntry = ttk.Entry(master=self.frameInputs,textvariable=self.BaseRate)        
        self.PaymentAmountLabel = ttk.Label(master=self.frameInputs,text="Payment Amount")
        self.PaymentAmountEntry = ttk.Entry(master=self.frameInputs,textvariable=self.PaymentAmount)        
        self.FrequencyLabel = ttk.Label(master=self.frameInputs,text="Frequency")
        self.FrequencyCbox = ttk.Combobox(master=self.frameInputs,textvariable=self.Frequency, values=self.FrequencyKeys)        
        
        #Components Grid Layout
        self.StartDateLabel.grid(row=0, column=0, sticky=tk.W, padx=2, pady=2)
        self.StartDateEntry.grid(row=0, column=1, sticky=tk.W, padx=2, pady=2)
        self.EndDateLabel.grid(row=1, column=0, sticky=tk.W, padx=2, pady=2)
        self.EndDateEntry.grid(row=1, column=1, sticky=tk.W, padx=2, pady=2)
        self.BegPrinLabel.grid(row=2, column=0, sticky=tk.W, padx=2, pady=2)
        self.BegPrinEntry.grid(row=2, column=1, sticky=tk.W, padx=2, pady=2)
        self.BaseRateLabel.grid(row=3, column=0, sticky=tk.W, padx=2, pady=2)
        self.BaseRateEntry.grid(row=3, column=1, sticky=tk.W, padx=2, pady=2)        
        self.PaymentAmountLabel.grid(row=4, column=0, sticky=tk.W, padx=2, pady=2)
        self.PaymentAmountEntry.grid(row=4, column=1, sticky=tk.W, padx=2, pady=2)        
        self.FrequencyLabel.grid(row=5, column=0, sticky=tk.W, padx=2, pady=2)
        self.FrequencyCbox.grid(row=5, column=1, sticky=tk.W, padx=2, pady=2)        
        #Frame Grid Layout
        self.frameInputs.grid(row=1, column=0, rowspan=3, columnspan=3, sticky=tk.W, padx=5, pady=5)
        #Other
        self.LastResult = None

    def saveResults(self):
        #Save Results to File
        f = filedialog.asksaveasfile(master=self, mode="w", filetypes=[("Json Files","*.json"),("Text Files","*.txt")])
        if f is not None:
            f.write(f"[")
            for i in self.LastResult:
                f.write(f"{i},\n")
            f.write(f"]\n")
            f.close()
        
    def calculate(self):
        try:
            sd = self.StartDate.get().split('-')
            ed = self.EndDate.get().split('-')
            sdate=date(int(sd[0]), int(sd[1]), int(sd[2]))
            edate=date(int(ed[0]), int(ed[1]), int(ed[2]))
            loan = LoanCalculator.Loan(principalAmount=float(self.BegPrin.get()),
                                   interestRate=float(self.BaseRate.get()), 
                                   startDate=sdate, 
                                   endDate=edate, 
                                   repayFrequency=self.Frequency.get(),
                                   repayAmount=float(self.PaymentAmount.get()))
            self.LastResult = LoanCalculator.calculateLoanRepayment(loan)
            print(self.LastResult)
        except Exception as e:
            print(f"Error: {e}")                        

if __name__=="__main__":
   '''
   generic Tk frame for Loan Repayment GUI - WIP
   '''
   window = LoanRepaymentUI()
   style = ttk.Style(window)
   style.map("TButton", foreground=[('pressed', 'blue'), ('active', 'blue')],
                        background=[('pressed', '!disabled', 'yellow'), ('active', 'green')])
   window.mainloop()