import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Device } from './divice'; // păstrează tipul existent sau aliniază-l cu scan.interface dacă e identic

@Injectable({ providedIn: 'root' })
export class OthersStoreService {
  private devicesSubject = new BehaviorSubject<Device[]>([]);

  devices$ = this.devicesSubject.asObservable();

  private apiUrl = 'http://127.0.0.1:8000/others';

  constructor(private http: HttpClient) {}

  getDevices(): Observable<Device[]> {
    return this.http.get<Device[]>(this.apiUrl);
  }

  setDevices(devices: Device[]): void {
    this.devicesSubject.next(devices);
  }

  getDevicesSnapshot(): Device[] {
    return this.devicesSubject.getValue();
  }
}
