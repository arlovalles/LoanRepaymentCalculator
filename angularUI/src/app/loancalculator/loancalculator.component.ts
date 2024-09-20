import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormGroup, FormBuilder, ReactiveFormsModule} from '@angular/forms';
import { CalculatorService } from '../calculator.service';
import { CalculationRequest } from '../CalculationRequest';
import { CalculationResult } from '../CalculationResult';

@Component({
  selector: 'app-loancalculator',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  styleUrl: './loancalculator.component.css',
  templateUrl:'./loancalculator.component.html'
})

export class LoancalculatorComponent {

  frequencies:string[] = ["MONTHLY", "WEEKLY", "QUARTERLY", "ANNUALLY"];
  crForm : FormGroup;
  selectedFrequency:string="";
  lastResult:CalculationResult[] = [];

  calculationRequest:CalculationRequest = { PrincipalAmount:0.00,
                                            InterestRateAnnual:0.00,
                                            StartDate:new Date(),
                                            EndDate:new Date(),
                                            RepaymentAmount:0.00,
                                            RepaymentFrequency:"" }

  constructor(private fb:FormBuilder, private calculatorService:CalculatorService){
    this.calculatorService = calculatorService;
    this.crForm = this.fb.group({
      principalAmount:'',
      interestRate:'',
      startDate:'',
      endDate:'',
      repayAmount:'',
      repayFrequency:''
    });
    
  }

  ngOnInit(){
    this.crForm.get("repayFrequency")?.valueChanges.subscribe(f => {
      this.onFrequencyChanged(f);
    })
  }

  onFrequencyChanged(value:string) {
    this.selectedFrequency = value;    
  }

  onSubmit():void {
    this.calculate();
  }

  calculate():void {

    this.calculationRequest = {
        PrincipalAmount:this.crForm.get("principalAmount")?.value,
        InterestRateAnnual:this.crForm.get("interestRate")?.value,
        StartDate:this.crForm.get("startDate")?.value,
        EndDate:this.crForm.get("endDate")?.value,
        RepaymentAmount:this.crForm.get("repayAmount")?.value,
        RepaymentFrequency:this.crForm.get("repayFrequency")?.value 
      };        
    
    console.log(this.calculationRequest);      
    this.calculatorService.calculation_post(this.calculationRequest);  

  }

}
