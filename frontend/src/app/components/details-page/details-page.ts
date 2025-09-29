import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-details-page',
  imports: [CommonModule],
  templateUrl: './details-page.html',
  styleUrl: './details-page.css',
})
export class DetailsPage {
  deviceId: string | null;
  devices: any;

  constructor(private route: ActivatedRoute, private router: Router) {
    this.deviceId = this.route.snapshot.paramMap.get('id');
  }

  toMain() {
    this.router.navigate(['']);
  }
}
