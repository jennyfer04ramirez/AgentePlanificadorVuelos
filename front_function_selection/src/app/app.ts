import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FunctionSelectionService } from './services/functionSelectionService/function-selection-service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; 
import { HttpClient } from '@angular/common/http';
type BotResponse = {
  session_id?: string;
  query: string;
  function: string;
  response: string;
  score: number;
  source: string;
};

type Msg = {
  role: 'user' | 'bot';
  text: string;
  meta?: { fn?: string; score?: number; source?: string };
};
@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CommonModule ,FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  // Cambia si tu backend está en otra URL
  apiUrl = 'http://localhost:8000/select';

  sessionId: string | null = null;
  topK = 4;

  loading = false;
  input = '';

  messages: Msg[] = [
    {
      role: 'bot',
      text: 'Hola ✈️🙂 ¿Qué deseas hacer? (buscar / reservar / cancelar)',
      meta: { fn: 'saludo' },
    },
  ];

  constructor(private http: HttpClient) {}

  send() {
    const text = this.input.trim();
    if (!text || this.loading) return;

    this.messages.push({ role: 'user', text });
    this.input = '';
    this.loading = true;

    const payload: any = { query: text, top_k: this.topK };
    if (this.sessionId) payload.session_id = this.sessionId;

    this.http.post<BotResponse>(this.apiUrl, payload).subscribe({
      next: (res) => {
        if (res.session_id) this.sessionId = res.session_id;

        this.messages.push({
          role: 'bot',
          text: res.response ?? '(sin respuesta)',
          meta: { fn: res.function, score: res.score, source: res.source },
        });

        this.loading = false;
        setTimeout(() => this.scrollToBottom(), 0);
      },
      error: (err) => {
        this.messages.push({
          role: 'bot',
          text: '❌ Error llamando al backend:'+ err?.message,
        });
        this.loading = false;
      },
    });
  }

  resetSession() {
    this.sessionId = null;
    this.messages = [
      {
        role: 'bot',
        text: 'Sesión reiniciada ✅ ¿Qué deseas hacer ahora?',
        meta: { fn: 'reset' },
      },
    ];
    this.input = '';
  }

  quick(text: string) {
    this.input = text;
    this.send();
  }

  private scrollToBottom() {
    const el = document.getElementById('chat-scroll');
    if (el) el.scrollTop = el.scrollHeight;
  }
}
