export interface CalculationRequest{    
    PrincipalAmount:number;
    InterestRateAnnual:number;
    StartDate:Date;
    EndDate:Date;
    RepaymentAmount:number;
    RepaymentFrequency:string;
}