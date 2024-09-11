from datetime import date
from dateutil.relativedelta import relativedelta

ALLOWABLE_REPAY_FREQUENCIES = ["MONTHLY", "WEEKLY", "QUARTERLY"]

class FREQUENCY:
    MONTHLY=relativedelta(months=+1)
    QUARTERLY=relativedelta(months=+3)
    WEEKLY=relativedelta(weeks=+1)
    SEMIANNUALLY=relativedelta(months=+6)
    ANNUALLY=relativedelta(years=+1)

FREQUENCY_LOOKUP={"MONTHLY":FREQUENCY.MONTHLY,
                  "QUARTERLY":FREQUENCY.QUARTERLY,
                  "WEEKLY":FREQUENCY.WEEKLY,
                  "SEMIANNUALLY":FREQUENCY.SEMIANNUALLY,
                  "ANNUALLY":FREQUENCY.ANNUALLY}

class Loan:
    principalAmount:float
    startDate:date
    endDate:date
    repayFrequency:str
    interestRate:float
    def __init__(self, principalAmount:float, interestRate:float, startDate:date, endDate:date, repayFrequency:str="MONTHLY"):
        self.principalAmount = principalAmount
        self.interestRate = interestRate
        self.startDate = startDate
        self.endDate = endDate
        self.repayFrequency = repayFrequency

    def __str__(self):
        return f"\nStart Date: {self.startDate}\nEndDate: {self.endDate}\nPrincipal: {self.principalAmount}\nInterestRate: {self.interestRate}\nRepayed: {self.repayFrequency}"

class LoanRepayment:
    eventDate:date
    principalBalance:float
    interestBalance:float
    interestEarned:float
    period:int
    repaymentAmount:float
    def __init__(self, eventDate:date, principalBalance:float, interestBalance:float, interestEarned:float, repaymentAmount:float, period:int):
        self.eventDate = eventDate
        self.principalBalance = principalBalance
        self.interestBalance = interestBalance
        self.interestEarned = interestEarned
        self.repaymentAmount = repaymentAmount
        self.period = period

    def __str__(self):
        return f"Date: {self.eventDate} Principal Balance: {self.principalBalance} InterestBalance: {self.interestBalance} Interest Earned: {self.interestEarned} Period: {self.period} RepaymentAmount: {self.repaymentAmount}"

def validate_Loan(loan:Loan):
    errorMessages={"Warnings":[], "Errors":[]}
    if loan.interestRate <= 0.00:
        errorMessages["Warnings"].append("\nInterest Rate should Not Be Less Than Or Equal To Zero.")
    if loan.principalAmount <= 0.00:
        errorMessages["Warnings"].append("\nPrincipal Amount should be Greater Than Equal to Zero.")
    if loan.startDate is None:
        errorMessages["Errors"].append("\nStartDate is Required. It cannot be None.")
    if loan.endDate is None:
        errorMessages["Errors"].append("\nEndDate is Required. It cannot be None.")
    if loan.startDate is not None and loan.endDate is not None and loan.endDate <= loan.startDate:
        errorMessages["Errors"].append("\nEndDate must be after the Start Date.")
    if loan.repayFrequency not in ALLOWABLE_REPAY_FREQUENCIES:
        errorMessages["Errors"].append("\nUnknwon Repayment Frequency.")
    if len(errorMessages["Warnings"]) > 0:
        raise RuntimeError(mergeErrorMessage(errorMessages["Warnings"]))
    if len(errorMessages["Errors"]) > 0:
        raise RuntimeError(mergeErrorMessage(errorMessages["Errors"]))

def calculateLoanRepayment(loan:Loan):
    repaymentFrequency=FREQUENCY_LOOKUP[loan.repayFrequency]
    currentDate = loan.startDate
    repayItems = []
    periodDays = 0
    PrincipalBalance = loan.principalAmount
    InterestBalance = 0.00 
    lastDate = currentDate
    payment=0.00
    while currentDate <= loan.endDate:        
        if currentDate > lastDate:
            periodDays = (currentDate - lastDate).days
            periodAccrued = CalculateInterest(principalAmount=PrincipalBalance, annualInterestRate=loan.interestRate, periodDays=periodDays)
            InterestBalance += periodAccrued
            #todo: fix this
            if PrincipalBalance > 0:
                if PrincipalBalance < 100.00:
                    prinPay = PrincipalBalance
                else:
                    prinPay=100.00
            else:
                prinPay = 0.00
        else:
            prinPay=0.00
            periodAccrued=0.00
                    
        PrincipalBalance -= prinPay
        intPay = periodAccrued
        payment = prinPay + intPay
        lastDate = currentDate
        currentDate = currentDate + repaymentFrequency
        if payment > 0:
            repayItems.append(LoanRepayment(eventDate=lastDate, 
                                repaymentAmount=payment,
                                principalBalance=PrincipalBalance, 
                                interestBalance=InterestBalance,
                                period=periodDays, 
                                interestEarned=periodAccrued))    
    
    return repayItems

def CalculateInterest(principalAmount:float=0, annualInterestRate:float=0.00, periodDays=1):
    dailyRate = annualInterestRate/365/100
    return principalAmount * dailyRate * periodDays

def mergeErrorMessage(messages:list=[]):
    result = ""
    result = result.join(messages)
    return result


if __name__ == '__main__':

    try:
        l = Loan(principalAmount=10000.00, interestRate=.0275, startDate=date(2022,1,15), endDate=date(2027,1,15), repayFrequency="MONTHLY")
        validate_Loan(l)
        for r in calculateLoanRepayment(l):
            print(r)
    except Exception as e:
        print(e, l)

"""     try:
        l = Loan(principalAmount=-10.00, interestRate=.0299, startDate=date(2028,1,15), endDate=date(2027,1,15), repayFrequency="MONTHLY")
        validate_Loan(l)
        print(calculateLoanRepayment(l))
    except Exception as e:
        print(e, l) """