import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-alert',
  imports: [],
  templateUrl: './alert.html',
  styleUrl: './alert.css',
})
export class Alert {
  constructor(private router: Router) {}
  toError() {
    this.router.navigate(['/details/1']);
  }
}
