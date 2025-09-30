import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { OthersStoreService } from '../../services/others';
import { Device } from '../../services/divice';
import { CommonModule } from '@angular/common';
import { PhoneService } from '../../services/phone';
import { PcStoreService } from '../../services/pc';
import { Observable, map } from 'rxjs';

@Component({
  selector: 'app-main-page',
  imports: [CommonModule],
  templateUrl: './main-page.html',
  styleUrls: ['./main-page.css'],
})
export class MainPage implements OnInit {
  errorAlert = false;
  othersData: any[] = [];

  // Observable-urile pentru fiecare tip de device
  othersData$!: Observable<any>;
  phoneData$!: Observable<any>;
  pcData$!: Observable<any>;

  constructor(
    private router: Router,
    private othersStore: OthersStoreService,
    private phoneStore: PhoneService,
    private pcStore: PcStoreService
  ) {}

  ngOnInit() {
    // Inițializează observables pentru fiecare tip de device
    this.othersData$ = this.othersStore.devices$;
    this.phoneData$ = this.phoneStore.devices$;
    this.pcData$ = this.pcStore.devices$;
  }

  // Getter pentru PC devices count
  get pcDevicesCount$(): Observable<number> {
    return this.pcData$.pipe(map((devices: any) => devices?.length || 0));
  }

  // Getter pentru Phone devices count
  get phoneDevicesCount$(): Observable<number> {
    return this.phoneData$.pipe(map((devices: any) => devices?.length || 0));
  }

  // Getter pentru Others devices count
  get othersDevicesCount$(): Observable<number> {
    return this.othersData$.pipe(map((devices: any) => devices?.length || 0));
  }

  // Getter pentru status PC (roșu dacă are issues, verde dacă nu)
  get pcCardStatus$(): Observable<string> {
    return this.pcData$.pipe(
      map((devices: any) => {
        if (!devices || devices.length === 0) return 'neutral';

        const hasIssues = devices.some(
          (device: any) =>
            device.security_analysis &&
            device.security_analysis.total_issues > 0
        );

        return hasIssues ? 'danger' : 'safe';
      })
    );
  }

  // Getter pentru status Phone
  get phoneCardStatus$(): Observable<string> {
    return this.phoneData$.pipe(
      map((devices: any) => {
        if (!devices || devices.length === 0) return 'neutral';

        const hasIssues = devices.some(
          (device: any) =>
            device.security_analysis &&
            device.security_analysis.total_issues > 0
        );

        return hasIssues ? 'danger' : 'safe';
      })
    );
  }

  // Getter pentru status Others
  get othersCardStatus$(): Observable<string> {
    return this.othersData$.pipe(
      map((devices: any) => {
        if (!devices || devices.length === 0) return 'neutral';

        const hasIssues = devices.some(
          (device: any) =>
            device.security_analysis &&
            device.security_analysis.total_issues > 0
        );

        return hasIssues ? 'danger' : 'safe';
      })
    );
  }

  toOthers() {
    this.router.navigate(['/others']);
  }

  toPC() {
    this.router.navigate(['/pc']);
  }

  toPhone() {
    this.router.navigate(['/phone']);
  }

  // Funcția care apelează API-ul pentru toate device-urile
  fetchOthersDevices() {
    this.othersStore.getDevices().subscribe({
      next: (response: any) => {
        console.log('Others:', response);
        this.othersStore.setDevices(response);
      },
    });

    this.phoneStore.getDevices().subscribe({
      next: (response: any) => {
        console.log('Phones:', response);
        this.phoneStore.setDevices(response);
      },
    });

    this.pcStore.getDevices().subscribe({
      next: (response: any) => {
        console.log('PCs:', response);
        this.pcStore.setDevices(response);
      },
    });
  }
}
