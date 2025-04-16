import {inject, Injectable, InjectionToken} from '@angular/core';
import {AppEnvironment} from '@models/environment';

const LOCAL_STORAGE = new InjectionToken<Storage>('Browser Storage', {
  providedIn: 'root',
  factory: () => localStorage,
});

@Injectable({
  providedIn: 'root',
})
export class StorageService {
  private readonly storage = inject<Storage>(LOCAL_STORAGE);

  get(key: string) {
    return this.storage.getItem(key);
  }

  set(key: string, value: string): void {
    this.storage.setItem(key, value);
  }

  remove(key: string): void {
    return this.storage.removeItem(key);
  }

  clear() {
    return this.storage.clear();
  }
}
