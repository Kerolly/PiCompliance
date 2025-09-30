import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Device } from './divice';

@Injectable({
  providedIn: 'root',
})
export class PcService {
  private apiUrl = 'http://127.0.0.1:8000/pc';

  constructor(private http: HttpClient) {}

  getPcDevices(): Observable<Device[]> {
    return this.http.get<Device[]>(this.apiUrl);
  }
}
