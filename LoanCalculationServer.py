from flask import Flask, request, render_template
from datetime import date
import LoanCalculator
import json

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Working!</p>"

@app.get("/loancalculation")
def loancalculation_get():
    return "<p>Hello, World!</p>"

@app.post("/loancalculation")
def loancalculation_post():
    result = None
    try:
        data = request.get_json()
        loan = LoanCalculator.Loan(principalAmount=float(data["PrincipalAmount"]), 
                                interestRate=float(data["InterestRateAnnual"]), 
                                startDate=format_date(data["StartDate"]), 
                                endDate=format_date(data["EndDate"]), 
                                repayAmount=float(data["RepaymentAmount"]), 
                                repayFrequency=data["RepaymentFrequency"])
        LoanCalculator.validate_Loan(loan)
        response = LoanCalculator.calculateLoanRepayment(loan) 
        print(response)
        result = render_template('LoanRepayment.html', data=response)
    except Exception as e:
        print(e)
        result = render_template('Error.html', error=e)
    return result 


def format_date(arg:str)->date:
     d = arg.split('-')
     return date(year=int(d[0]), month=int(d[1]), day=int(d[2]))
     