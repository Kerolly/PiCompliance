import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Device } from './divice';

@Injectable({
  providedIn: 'root',
})
export class OthersService {
  private apiUrl = 'http://127.0.0.1:8000/others';

  constructor(private http: HttpClient) {}

  getOtherDevices(): Observable<Device[]> {
    return this.http.get<Device[]>(this.apiUrl);
  }
}
