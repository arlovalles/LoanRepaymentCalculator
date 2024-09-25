import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { CalculationRequest } from '../model/CalculationRequest';
import { CalculationResult } from '../model/CalculationResult';
import { Observable } from 'rxjs';
import { MessageService } from './message.service';

@Injectable({
  providedIn: 'root'
})

export class CalculatorService {
  private url='http://127.0.0.1:5000/loancalculation';
  constructor(private http:HttpClient, private messageService:MessageService) {}

  calculate(calculationRequest:CalculationRequest):Observable<CalculationResult[]>{    
    const params = new HttpParams()
      .set('principalAmount', calculationRequest.PrincipalAmount)
      .set('interestRate', calculationRequest.InterestRate)
      .set('startDate', calculationRequest.StartDate.toString())
      .set('endDate', calculationRequest.EndDate.toString())
      .set('repayAmount', calculationRequest.RepaymentAmount)
      .set('repayFrequency', calculationRequest.RepaymentFrequency);

      return this.http.get<CalculationResult[]>(this.url, {params});
  }

  private log(message: string) {
    this.messageService.add(`CalcService: ${message}`);
  }

}
