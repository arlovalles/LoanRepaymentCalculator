from datetime import date
from dateutil.relativedelta import relativedelta

ALLOWABLE_REPAY_FREQUENCIES = ["MONTHLY", "WEEKLY", "QUARTERLY"]

class FREQUENCY:
    '''
    DESCRIPTION: FREQUENCY class is to provide a static list of supported frequencies for repayment calculations. 
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
    DESCRIPTION: Basic Loan Object - Financial Instrument with basic properties.
    PROPERTIES:
        principalAmount:float
        interestRate:float
        startDate:date
        endDate:date
        repayFrequency:str  #["MONTHLY", "WEEKLY", "QUARTERLY"]
    '''
    principalAmount:float
    startDate:date
    endDate:date
    repayAmount:float
    repayFrequency:str
    interestRate:float
    def __init__(self, principalAmount:float, interestRate:float, startDate:date, endDate:date, repayAmount:float, repayFrequency:str="MONTHLY"):
        self.principalAmount = principalAmount
        self.interestRate = interestRate
        self.startDate = startDate
        self.endDate = endDate
        self.repayAmount = repayAmount
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
    interestRepaymentAmount:float
    principalRepaymentAmount:float

    def __init__(self, eventDate:date, principalBalance:float, interestBalance:float, interestEarned:float, period:int, interestRepaymentAmount:float, principalRepaymentAmount:float):
        self.eventDate = eventDate
        self.principalBalance = principalBalance
        self.interestBalance = interestBalance
        self.interestEarned = interestEarned
        self.repaymentAmount = interestRepaymentAmount + principalRepaymentAmount
        self.interestRepaymentAmount = interestRepaymentAmount
        self.principalRepaymentAmount = principalRepaymentAmount
        self.period = period

    def __str__(self):
        return f"Date: {self.eventDate} Principal Balance: {self.principalBalance} Interest Balance: {self.interestBalance} Period Interest Earned: {self.interestEarned} Period: {self.period} Payment Amount: (P){self.principalRepaymentAmount} + (I){self.interestRepaymentAmount} = {self.repaymentAmount}"

def validate_Loan(loan:Loan, ignoreWarnings:bool=False):
    '''
    DESCRIPTION: Loan Validation routine. Will raise RuntimeError with messages if errors are detected. 
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
    DESCRIPTION: Loan Repayment Calculation routine. Calculates Repayment Cashflow. 
    '''
    repaymentFrequency=FREQUENCY_LOOKUP[loan.repayFrequency]
    currentDate = loan.startDate
    repayItems = []
    periodDays = 0
    PrincipalBalance = loan.principalAmount
    InterestBalance = 0.00 
    lastDate = currentDate
    while currentDate <= loan.endDate:        
        if currentDate > lastDate:
            periodDays = (currentDate - lastDate).days
            periodAccrued = CalculateInterest(principalAmount=PrincipalBalance, annualInterestRate=loan.interestRate, periodDays=periodDays)
            InterestBalance += periodAccrued
            if InterestBalance > loan.repayAmount:
                intPay = loan.repayAmount
            else:
                intPay = InterestBalance                        
            
            if PrincipalBalance <= 0:
                prinPay=0.00
            elif PrincipalBalance < prinPay:
                prinPay=PrincipalBalance
            else:
                prinPay = loan.repayAmount - intPay

        else:
            prinPay = 0.00
            intPay = 0.00
            periodAccrued = 0.00
                                        
        InterestBalance -= intPay
        PrincipalBalance -= prinPay        
        lastDate = currentDate
        currentDate = currentDate + repaymentFrequency
        
        if prinPay > 0 or intPay >0:
            repayItems.append(LoanRepayment(eventDate=lastDate, 
                                principalBalance=PrincipalBalance, 
                                interestBalance=InterestBalance,
                                period=periodDays, 
                                interestEarned=periodAccrued,
                                interestRepaymentAmount=intPay,
                                principalRepaymentAmount=prinPay))    
    
    return repayItems

def CalculateInterest(principalAmount:float=0, annualInterestRate:float=0.00, periodDays:int=1):
    '''
    DESCRIPTION: Simple Interest Calculation
    '''
    dailyRate = annualInterestRate/365/100
    return principalAmount * dailyRate * periodDays

def mergeMessages(messages:list=[]):
    '''
    DESCRIPTION: Merge List of Messages into a single string for reporting.
    '''
    result = ""
    result = result.join(messages)
    return result


if __name__ == '__main__':
    '''
    Example for testing
    '''
    try:
        ln = Loan(principalAmount=10000.00, interestRate=.0275, startDate=date(2022,1,15), endDate=date(2027,1,15), repayAmount=1250.00, repayFrequency="MONTHLY")
        validate_Loan(ln)
        for repayEvent in calculateLoanRepayment(ln):
            print(repayEvent)
    except Exception as e:
        print(e, ln)
