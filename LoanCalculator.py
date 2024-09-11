from datetime import date
from dateutil.relativedelta import relativedelta

ALLOWABLE_REPAY_FREQUENCIES = ["MONTHLY", "WEEKLY", "QUARTERLY"]

class FREQUENCY:
    '''
    FREQUENCY class is to provide a static list of supported frequencies for repayment calculations. 
    Can use module level dictionary FREQUENCY_LOOKUP to get appropriate relativeDelta. 
    
    Example: repaymentFrequency=FREQUENCY_LOOKUP["MONTHLY"] 
             nextDate = currentDate + repaymentFrequency

    '''
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
    '''
    Basic Loan Object - Financial Instrument with basic properties.
    principalAmount:float
    interestRate:float
    startDate:date
    endDate:date
    repayFrequency:str  #["MONTHLY", "WEEKLY", "QUARTERLY"]
    '''
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
    '''
    Repayment Event:
        eventDate:date
        principalBalance:float
        interestBalance:float
        interestEarned:float
        period:int
        repaymentAmount:float        
    '''
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
        return f"Date: {self.eventDate} Principal: {self.principalBalance} Total Interest: {self.interestBalance} Period Interest Earned: {self.interestEarned} Period: {self.period} Payment Amount: {self.repaymentAmount}"

def validate_Loan(loan:Loan, ignoreWarnings:bool=False):
    '''
    Loan Validation routine. Will raise RuntimeError with messages if errors are detected. 
    '''
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
    if len(errorMessages["Errors"]) > 0:
        raise RuntimeError(mergeMessages(errorMessages["Errors"]))
    if len(errorMessages["Warnings"]) > 0 and not ignoreWarnings:
        raise RuntimeError(mergeMessages(errorMessages["Warnings"]))    

def calculateLoanRepayment(loan:Loan):
    '''
    Loan Repayment Calculation routine. Calculates Repayment Cashflow. 
    '''
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
            intPay = InterestBalance
            InterestBalance += periodAccrued
            #todo: fix this
            if PrincipalBalance > 0:
                if PrincipalBalance < 100.00 or currentDate >= loan.endDate:
                    prinPay = PrincipalBalance
                else:
                    prinPay=100.00
            else:
                prinPay = 0.00
        else:
            prinPay = 0.00
            intPay = 0.00
            periodAccrued = 0.00
                    
        PrincipalBalance -= prinPay        
        payment = prinPay + intPay
        lastDate = currentDate
        currentDate = currentDate + repaymentFrequency
        if PrincipalBalance > 0 or InterestBalance > 0:
            repayItems.append(LoanRepayment(eventDate=lastDate, 
                                repaymentAmount=payment,
                                principalBalance=PrincipalBalance, 
                                interestBalance=InterestBalance,
                                period=periodDays, 
                                interestEarned=periodAccrued))    
    
    return repayItems

def CalculateInterest(principalAmount:float=0, annualInterestRate:float=0.00, periodDays=1):
    '''
    Simple Interest Calculation
    '''
    dailyRate = annualInterestRate/365/100
    return principalAmount * dailyRate * periodDays

def mergeMessages(messages:list=[]):
    '''
    Merge List of Messages into a single string for reporting.
    '''
    result = ""
    result = result.join(messages)
    return result


if __name__ == '__main__':
    '''
    Example for testing
    '''
    try:
        ln = Loan(principalAmount=10000.00, interestRate=.0275, startDate=date(2022,1,15), endDate=date(2027,1,15), repayFrequency="MONTHLY")
        validate_Loan(ln)
        for repayEvent in calculateLoanRepayment(ln):
            print(repayEvent)
    except Exception as e:
        print(e, ln)
