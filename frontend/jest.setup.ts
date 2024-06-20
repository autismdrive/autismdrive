import {Crypto} from '@peculiar/webcrypto';

(window as any).msCrypto = new Crypto();
(window as any).crypto = new Crypto();
(window as any).getComputedStyle = () => ({
  getPropertyValue: prop => {
    return '';
  },
});
