import {WindowService} from '@services/window/window.service';
import {DeviceDetectorService} from 'ngx-device-detector';

export const scrollToTop = function (deviceDetectorService: DeviceDetectorService, windowService: WindowService) {
  windowService.window.scroll({
    top: 0,
    left: 0,
    behavior: 'smooth',
  });
  if (deviceDetectorService.browser === 'Safari') {
    windowService.window.scroll(0, 0);
  } else {
    windowService.window.scroll({behavior: 'smooth', top: 0});
  }
};

export const scrollToFirstInvalidField = function (
  deviceDetectorService: DeviceDetectorService,
  windowService: WindowService,
) {
  const el: HTMLElement = document.querySelector('mat-form-field.ng-invalid');
  if (el) {
    if (deviceDetectorService.browser === 'Safari') {
      windowService.window.scroll(0, el.offsetTop - 200);
    } else {
      windowService.window.scroll({behavior: 'smooth', top: el.offsetTop - 200});
    }
  }
};
