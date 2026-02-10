import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class FunctionSelectionService {
  private readonly apiUrl = 'http://localhost:8000/select_function_langchain';
  // cambia host/puerto si es necesario

  constructor(private readonly http: HttpClient) {}

  selectFunction(query: string, topK: number = 3): Observable<any> {
    return this.http.post(this.apiUrl, {
      query: query,
      top_k: topK
    });
  }  
}
