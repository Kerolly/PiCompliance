import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { OthersStoreService } from '../../services/others';
import { Device } from '../../services/divice';
import { AsyncPipe } from '@angular/common';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-others-page',
  standalone: true,
  imports: [CommonModule, AsyncPipe],
  templateUrl: './details-page.html',
  styleUrls: ['./details-page.css'],
})
export class DetailsPage implements OnInit {
  othersData$!: Observable<any>;

  constructor(
    private router: Router,
    private othersStore: OthersStoreService
  ) {}

  ngOnInit() {
    this.othersData$ = this.othersStore.devices$; // inițializare după ce constructorul rulează
    this.othersStore.getDevices().subscribe((devices) => {
      this.othersStore.setDevices(devices);
    });
  }

  toMain() {
    this.router.navigate(['']);
  }
}
