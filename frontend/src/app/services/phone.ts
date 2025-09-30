import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Device } from './divice';

@Injectable({
  providedIn: 'root',
})
export class PhoneService {
  private apiUrl = 'http://127.0.0.1:8000/phone';

  constructor(private http: HttpClient) {}

  getPhoneDevices(): Observable<Device[]> {
    return this.http.get<Device[]>(this.apiUrl);
  }
}
