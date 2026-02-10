import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FunctionSelectionService } from './services/functionSelectionService/function-selection-service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; 
@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CommonModule ,FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  query: string = '';
  loading = false;
  results: any[] = [];

  constructor(private readonly fsService: FunctionSelectionService) {}

  search() {
    if (!this.query.trim()) return;

    this.loading = true;
    this.results = [];

    this.fsService.selectFunction(this.query, 3).subscribe({
      next: (res) => {
        this.results = res.results;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
        alert('Error consultando la API');
      }
    });
  }
}
