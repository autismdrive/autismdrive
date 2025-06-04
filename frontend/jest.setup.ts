/* eslint-disable @typescript-eslint/no-explicit-any */
import {BrowserAnimationsModule, NoopAnimationsModule} from '@angular/platform-browser/animations';
import {Crypto} from '@peculiar/webcrypto';
import {ngMocks} from 'ng-mocks';

(window as any).msCrypto = new Crypto();
(window as any).crypto = new Crypto();
(window as any).getComputedStyle = () => ({
  getPropertyValue: () => {
    return '';
  },
});
// @ts-expect-error Zone.js patches MutationObserver in a way that is not compatible with happy-dom
(window as any).MutationObserver = window[Zone.__symbol__('MutationObserver')];

ngMocks.globalReplace(BrowserAnimationsModule, NoopAnimationsModule);
