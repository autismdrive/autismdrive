import {inject, Injectable} from '@angular/core';
import {LOCAL_STORAGE} from '@app/tokens';

@Injectable({
  providedIn: 'root',
})
export class StorageService {
  private readonly storage = inject<Storage>(LOCAL_STORAGE);

  get(key: string) {
    console.log('StorageService > get > key:', key, 'value:', this.storage.getItem(key));
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
