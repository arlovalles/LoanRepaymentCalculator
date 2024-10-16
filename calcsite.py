from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from pydantic import BaseModel, Field
from datetime import date
import LoanCalculator


app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:4200",
    "http://127.0.0.1:4200",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoanQueryParameters(BaseModel):
    principalAmount: float = Field(default=0.00, gt=0, description="Loan beginning principal amount")
    interestRate: float = Field(default=0.00, gt=0, description="Annual Interest Rate")
    startDate: str = Field(default=date.today(), description="Loan Start Date as (yyyy-mm-dd)")
    endDate: str = Field(default=date.today(), description="Loan End Date as (yyyy-mm-dd)")
    repayAmount: float = Field(default=0.00, ge=0, description="Expected regular payment amount.")
    repayFrequency: str = Field(default="MONTHLY", description="Must be one of these strings [MONTHLY, QUARTERLY, WEEKLY, SEMIANNUALLY, ANNUALLY]")

@app.get("/")
async def root():
    return {"message":"Loan Calculator Site",
            "url":"http://127.0.0.1:8000/loancalculator?principalAmount=12500&interestRate=2.59&startDate=2024-01-15&endDate=2028-02-15&repayAmount=550&repayFrequency=MONTHLY"
            }

@app.get("/loancalculator")
async def calculate(filterQuery:Annotated[LoanQueryParameters, Query()]):
    return LoanCalculator.calculateLoanRepayment(
                LoanCalculator.Loan(
                        principalAmount=filterQuery.principalAmount, 
                        interestRate=filterQuery.interestRate, 
                        startDate=format_date(filterQuery.startDate), 
                        endDate=format_date(filterQuery.endDate), 
                        repayAmount=filterQuery.repayAmount, 
                        repayFrequency=filterQuery.repayFrequency
                        ))

def format_date(arg:str)->date:
     d = arg.split('-')
     return date(year=int(d[0]), month=int(d[1]), day=int(d[2]))

if __name__ == '__main__':
    pass