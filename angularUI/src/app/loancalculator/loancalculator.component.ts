import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormGroup, FormBuilder, ReactiveFormsModule} from '@angular/forms';
import { CalculatorService } from '../services/calculator.service';
import { CalculationRequest } from '../model/CalculationRequest';
import { CalculationResult} from '../model/CalculationResult';
import { MessageService } from '../services/message.service';

@Component({
  selector: 'app-loancalculator',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  styleUrl: './loancalculator.component.css',
  templateUrl:'./loancalculator.component.html'
})

export class LoancalculatorComponent {

  protected frequencies:string[] = ["MONTHLY", "WEEKLY", "QUARTERLY", "ANNUALLY"];
  protected crForm : FormGroup;
  protected selectedFrequency:string="";
  protected calcResults:CalculationResult[]=[];
  private dummyResult:CalculationResult = { date:"2024-01-01",
                                    PrincipalBalance:999.99,
                                    InterestBalance:88.88,
                                    PeriodInterestEarned:123.45,
                                    RepaymentAmount:2.99,
                                    InterestRepaymentAmount:1.99,
                                    PrincipalRepaymentAmount:1.00,
                                    Period:30};

  private calculationRequest:CalculationRequest = { PrincipalAmount:0.00,
                                            InterestRate:0.00,
                                            StartDate:"",
                                            EndDate:"",
                                            RepaymentAmount:0.00,
                                            RepaymentFrequency:""};

  constructor(private fb:FormBuilder, private calculatorService:CalculatorService, private messageService:MessageService){
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

  SendMessage(message:string, clearBuffer:boolean=false):void {
    if (clearBuffer) {
      this.messageService.clear();
    }
    this.messageService.add(message);
  }

  onAddDummyResult():void {
    this.calcResults.push(this.dummyResult);
    this.SendMessage("Entries: " + this.calcResults.length, true);
  }

  onClearOutput():void {
    this.calcResults = [];
    this.messageService.clear();
  }

  onCalculate():void {
    this.calculationRequest = {
      PrincipalAmount:this.crForm.get("principalAmount")?.value,
      InterestRate:this.crForm.get("interestRate")?.value,
      StartDate:this.crForm.get("startDate")?.value,
      EndDate:this.crForm.get("endDate")?.value,
      RepaymentAmount:this.crForm.get("repayAmount")?.value,
      RepaymentFrequency:this.crForm.get("repayFrequency")?.value 
    };        

    this.onClearOutput();

    this.calculatorService.calculate(this.calculationRequest).subscribe({
      next: (value:CalculationResult[]) => {
          this.calcResults = Array.from(JSON.parse(value.toString()));        
      },
      error: e => this.SendMessage("Error -> " + e.message),
      complete:() => this.SendMessage("Entries: " + this.calcResults.length)
    });

    
  }
  
}
