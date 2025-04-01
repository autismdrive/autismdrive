import {afterNextRender, Injectable, NgZone} from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class IntervalService {
  interval: number = null;

  constructor(private ngZone: NgZone) {}

  setInterval(callback: () => void, time: number) {
    this.ngZone.runOutsideAngular(() => {
      afterNextRender(() => {
        this.interval = window.setInterval(() => {
          this.ngZone.run(callback);
        }, time);
      });
    });
  }

  clearInterval() {
    afterNextRender(() => {
      window.clearInterval(this.interval);
    });
  }
}
