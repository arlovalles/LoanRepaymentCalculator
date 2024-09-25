from flask import Flask, request, render_template
from datetime import date
import LoanCalculator

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route("/")
def index():
    return "<p>Server is up and working!</p>"

@app.get("/loancalculation/")
def loancalculation_get(principalAmount:float=None, interestRate:float=None, startDate:str=None, endDate:str=None, repayAmount:float=None, repayFrequency:str=None):
    result = None
    showRequestHeaders(request.headers)
    try:
        if request.args.get("principalAmount") is not None:
            principalAmount = float(request.args.get("principalAmount"))
        if request.args.get("interestRate") is not None:
            interestRate = float(request.args.get("interestRate"))
        if request.args.get("startDate") is not None:
            startDate = request.args.get("startDate")
        if request.args.get("endDate") is not None:
            endDate = request.args.get("endDate")
        if request.args.get("repayAmount") is not None:
            repayAmount = float(request.args.get("repayAmount"))
        if request.args.get("repayFrequency") is not None:
            repayFrequency = request.args.get("repayFrequency")
        if principalAmount is not None and interestRate is not None and startDate is not None and endDate is not None and repayAmount is not None and repayFrequency is not None:            
            validateIncomingParameters(principalAmount, interestRate, startDate, endDate, repayAmount, repayFrequency)
            data = calculate(principalAmount=principalAmount, 
                                      interestRate=interestRate, 
                                      startDate=format_date(startDate), 
                                      endDate=format_date(endDate), 
                                      repayAmount=repayAmount, 
                                      repayFrequency=repayFrequency)
            #result = render_template('LoanRepayment.html', data=data)
            result = data
        else:
            #result = render_template('LoanRepayment.html', data=None)
            result = None
    except Exception as e:
        print(e)
        result = render_template('Error.html', error=e)
    
    return result

def validateIncomingParameters(principalAmount:float, interestRate:float, startDate:str, endDate:str, repayAmount:float, repayFrequency:str):
    messages=""    
    if not bool(startDate.strip()):
        messages = messages + f"startDate is Required. "
    if not bool(endDate.strip()):
        messages = messages + f"endDate is Required. "
    if principalAmount <= 0:
        messages = messages + f"principal must be Positive. "
    if interestRate < 0:
        messages = messages + f"Negative interestRate is not Allowed. "
    if repayAmount < 0:
        messages = messages + f"Negative repaymentAmount is not Allowed. "
    if not bool(repayFrequency.strip()):
        messages = messages + f"repaymentFrequency is Required. "
    if bool(messages.strip()):
        raise ValueError(messages)
    return

def calculate(startDate:date, endDate:date, principalAmount:float=0.00, interestRate:float=0.00, repayAmount:float=0.00, repayFrequency:str=""):
    result = None
    loan = LoanCalculator.Loan(principalAmount=principalAmount, 
                                    interestRate=interestRate, 
                                    startDate=startDate, 
                                    endDate=endDate, 
                                    repayAmount=repayAmount, 
                                    repayFrequency=repayFrequency)
    LoanCalculator.validate_Loan(loan)
    result = LoanCalculator.calculateLoanRepayment(loan) 
    return result

def format_date(arg:str)->date:
     d = arg.split('-')
     return date(year=int(d[0]), month=int(d[1]), day=int(d[2]))

def showRequestHeaders(headers):
    print(headers)

'''
This module needs to be started using flask.
Example:  flask --app LoanCalculationServer run --debug
'''
if __name__ == '__main__':
    pass     