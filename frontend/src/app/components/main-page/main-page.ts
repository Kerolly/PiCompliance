import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { OthersStoreService } from '../../services/others';
import { Device } from '../../services/divice';
import { CommonModule } from '@angular/common';
import { PhoneService } from '../../services/phone';
import { PcStoreService } from '../../services/pc';

@Component({
  selector: 'app-main-page',
  imports: [CommonModule],
  templateUrl: './main-page.html',
  styleUrls: ['./main-page.css'],
})
export class MainPage {
  errorAlert = false;
  othersData: Device[] = [];

  constructor(
    private router: Router,
    private othersStore: OthersStoreService,
    private phoneStore: PhoneService,
    private pcStore: PcStoreService
  ) {}

  pc = { status: 'active', message: 'Online' };
  phone = { status: 'inactive', message: 'Offline' };
  other = { status: 'active', message: 'Online' };

  toOthers() {
    this.router.navigate(['/others']);
  }
  toPC() {
    this.router.navigate(['/pc']);
  }
  toPhone() {
    this.router.navigate(['/phone']);
  }

  // Funcția care apelează API-ul pentru Others
  fetchOthersDevices() {
    this.othersStore.getDevices().subscribe({
      next: (response) => {
        console.log(response);
      },
    });
    this.phoneStore.getDevices().subscribe({
      next: (response) => {
        console.log(response);
      },
    });
    this.pcStore.getDevices().subscribe({
      next: (response) => {
        console.log(response);
      },
    });
  }
}
