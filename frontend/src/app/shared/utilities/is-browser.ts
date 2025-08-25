import {isPlatformBrowser} from '@angular/common';
import {inject, PLATFORM_ID} from '@angular/core';

export const isBrowser = () => {
  const platformId = inject(PLATFORM_ID);
  return isPlatformBrowser(platformId);
};
