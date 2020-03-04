import { AfterViewInit, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { UserDataSource } from '../_models/user_data_source';
import { ApiService } from '../_services/api/api.service';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { debounceTime, distinctUntilChanged, tap } from 'rxjs/operators';
import { merge } from 'rxjs/internal/observable/merge';
import { fromEvent } from 'rxjs/internal/observable/fromEvent';
import { Router } from '@angular/router';


@Component({
  selector: 'app-user-admin',
  templateUrl: './user-admin.component.html',
  styleUrls: ['./user-admin.component.scss']
})
export class UserAdminComponent implements OnInit, AfterViewInit {

  dataSource: UserDataSource;
  displayedColumns = ['id', 'role', 'email', 'last_updated', 'registration_date', 'last_login', 'participants'];
  default_page_size = 10;

  @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;
  @ViewChild(MatSort, {static: true}) sort: MatSort;
  @ViewChild('input', {static: true}) input: ElementRef;

  constructor(
    private api: ApiService,
    private router: Router
  ) { }

  ngOnInit() {
    this.dataSource = new UserDataSource(this.api);
    this.dataSource.loadUsers('', 'email', 'asc',
      0, this.default_page_size);
  }

  onRowClicked(row) {
    this.router.navigate(['admin/user', row['id']]);
  }

  ngAfterViewInit() {

    // server-side search
    fromEvent(this.input.nativeElement, 'keyup')
      .pipe(
        debounceTime(150),
        distinctUntilChanged(),
        tap(() => {
          this.paginator.pageIndex = 0;
          this.loadUsers();
        })
      )
      .subscribe();

    // reset the paginator after sorting
    this.sort.sortChange.subscribe(() => this.paginator.pageIndex = 0);

    merge(this.sort.sortChange, this.paginator.page).pipe(
      tap(() => this.loadUsers())
    ).subscribe();

  }

  loadUsers() {
    this.dataSource.loadUsers(this.input.nativeElement.value, this.sort.active, this.sort.direction,
      this.paginator.pageIndex, this.paginator.pageSize);
  }

}
