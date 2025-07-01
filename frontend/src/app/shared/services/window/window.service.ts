import {DOCUMENT, isPlatformBrowser} from '@angular/common';
import {Inject, Injectable, PLATFORM_ID} from '@angular/core';
import {mockWindowFactory} from '@app/shared/fixtures/mock-window';

@Injectable({
  providedIn: 'root',
})
export class WindowService {
  _window: Window & typeof globalThis;

  constructor(
    @Inject(DOCUMENT) private document: Document,
    @Inject(PLATFORM_ID) private platformId: Object,
  ) {
    if (isPlatformBrowser(this.platformId)) {
      this._window = this.document.defaultView;
    } else {
      // For SSR, return a fake window-like object.
      this._window = mockWindowFactory() as unknown as Window & typeof globalThis;
    }
  }

  get window(): Window & typeof globalThis {
    return this._window;
  }
}
