import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PcStoreService } from '../../services/pc';
import { Device } from '../../services/divice';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-pc-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './pc-page.html',
  styleUrls: ['./pc-page.css'],
})
export class PcPage implements OnInit {
  pcData$!: Observable<any>;

  constructor(private router: Router, private pcStore: PcStoreService) {}

  ngOnInit() {
    // Fetch de la API și setăm BehaviorSubject
    this.pcStore.getDevices().subscribe((devices) => {
      this.pcStore.setDevices(devices);
    });

    // Observable direct pentru template
    this.pcData$ = this.pcStore.devices$;
  }

  toMain() {
    this.router.navigate(['']);
  }
}
