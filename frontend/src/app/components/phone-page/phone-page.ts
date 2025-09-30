import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PhoneService } from '../../services/phone';
import { Device } from '../../services/divice';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-phone-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './phone-page.html',
  styleUrl: './phone-page.css',
})
export class PhonePage implements OnInit {
  phoneData$!: Observable<any>;

  constructor(private router: Router, private phoneStore: PhoneService) {}

  ngOnInit() {
    // Fetch de la API și setăm BehaviorSubject
    this.phoneStore.getDevices().subscribe((devices) => {
      this.phoneStore.setDevices(devices);
    });

    // Observable direct pentru template
    this.phoneData$ = this.phoneStore.devices$;
  }

  toMain() {
    this.router.navigate(['']);
  }
}
