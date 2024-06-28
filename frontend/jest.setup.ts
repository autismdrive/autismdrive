import {BrowserAnimationsModule, NoopAnimationsModule} from '@angular/platform-browser/animations';
import {Crypto} from '@peculiar/webcrypto';
import {ngMocks} from 'ng-mocks';

(window as any).msCrypto = new Crypto();
(window as any).crypto = new Crypto();
(window as any).getComputedStyle = () => ({
  getPropertyValue: prop => {
    return '';
  },
});

ngMocks.globalReplace(BrowserAnimationsModule, NoopAnimationsModule);
