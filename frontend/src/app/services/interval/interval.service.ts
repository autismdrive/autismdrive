import { Injectable, NgZone } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class IntervalService {
  interval: number;

  constructor(private ngZone: NgZone) {
  }

  setInterval(callback: () => void, time: number) {
    this.ngZone.runOutsideAngular(() => {
      this.interval = window.setInterval(() => {
        this.ngZone.run(callback);
      }, time);
    });
  }

  clearInterval() {
    window.clearInterval(this.interval);
  }
}
