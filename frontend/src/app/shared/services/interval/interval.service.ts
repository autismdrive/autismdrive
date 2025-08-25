import {Injectable, NgZone} from '@angular/core';
import {WindowService} from '@services/window/window.service';

@Injectable({
  providedIn: 'root',
})
export class IntervalService {
  interval: number = null;

  constructor(
    private ngZone: NgZone,
    private windowService: WindowService,
  ) {}

  setInterval(callback: () => void, time: number) {
    this.ngZone.runOutsideAngular(() => {
      this.interval = this.windowService.window.setInterval(() => {
        this.ngZone.run(callback);
      }, time);
    });
  }

  clearInterval() {
    this.windowService.window.clearInterval(this.interval);
  }
}
