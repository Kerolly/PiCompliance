import { CommonModule } from '@angular/common';
import { Component, HostListener } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Alert } from '../../shared/alert/alert';

@Component({
  selector: 'app-main-page',
  imports: [CommonModule, RouterLink, Alert],
  templateUrl: './main-page.html',
  styleUrl: './main-page.css',
})
export class MainPage {
  errorAlert = false;

  Devices = [
    {
      id: 1,
      name: 'Printer',
      img: '/printer.png',
      status: 'danger',
      message: '⚠ Vulnerable',
    },
    {
      id: 2,
      name: 'Phone',
      img: '/phone.png',
      status: 'success',
      message: '✅ Secure',
    },
    {
      id: 3,
      name: 'Laptop',
      img: '/laptop.png',
      status: 'success',
      message: '✅ Secure',
    },
    {
      id: 4,
      name: 'Router',
      img: '/router.png',
      status: 'danger',
      message: '⚠ Open Ports',
    },
    {
      id: 5,
      name: 'Smart TV',
      img: '/tv.png',
      status: 'success',
      message: '✅ Secure',
    },
  ];

  @HostListener('document:keydown', ['$event'])
  handleKeydown(event: KeyboardEvent) {
    if (event.key === 'k') {
      this.errorAlert = !this.errorAlert;
    }
  }
}
