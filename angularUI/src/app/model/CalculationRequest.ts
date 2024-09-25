export interface CalculationRequest{    
    PrincipalAmount:number;
    InterestRate:number;
    StartDate:string;
    EndDate:string;
    RepaymentAmount:number;
    RepaymentFrequency:string;
}