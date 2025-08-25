import {CollectionViewer} from '@angular/cdk/collections';
import {DataSource} from '@angular/cdk/table';
import {signal, WritableSignal} from '@angular/core';
import {ApiService} from '@app/shared/services/api/api.service';
import {lastValueFrom, Observable, of} from 'rxjs';
import {User} from './user';

export class UserDataSource implements DataSource<User> {
  private users: WritableSignal<User[]> = signal(undefined);
  private count: WritableSignal<number> = signal(undefined);
  private loading: WritableSignal<boolean> = signal(undefined);

  constructor(private api: ApiService) {}

  connect(collectionViewer: CollectionViewer): Observable<User[]> {
    return of(this.users());
  }

  disconnect(collectionViewer: CollectionViewer): void {
    // Destroy the signals when disconnecting
    this.users.set(undefined);
    this.count.set(undefined);
    this.loading.set(undefined);
  }

  async loadUsers(filter = '', sort = 'email', sortOrder = 'asc', pageNumber = 0, pageSize = 10) {
    this.loading.set(true);

    try {
      const results = await lastValueFrom(this.api.findUsers(filter, sort, sortOrder, pageNumber, pageSize));
      this.users.set(results.items);
      this.count.set(results.total);
    } catch (error) {
      this.users.set(undefined);
      this.count.set(0);
    }

    this.loading.set(false);
  }
}
