import {DeviceDetectorService} from 'ngx-device-detector';

export const scrollToTop = function (deviceDetectorService: DeviceDetectorService) {
  window.scroll({
    top: 0,
    left: 0,
    behavior: 'smooth',
  });
  if (deviceDetectorService.browser === 'Safari') {
    window.scroll(0, 0);
  } else {
    window.scroll({behavior: 'smooth', top: 0});
  }
};

export const scrollToFirstInvalidField = function (deviceDetectorService: DeviceDetectorService) {
  const el: HTMLElement = document.querySelector('mat-form-field.ng-invalid');
  if (el) {
    if (deviceDetectorService.browser === 'Safari') {
      window.scroll(0, el.offsetTop - 200);
    } else {
      window.scroll({behavior: 'smooth', top: el.offsetTop - 200});
    }
  }
};
