import { Component, OnInit, ViewChild } from '@angular/core';
import {MatTableDataSource} from '@angular/material/table';
import { ApiService } from '../_services/api/api.service';
import { MatSort } from '@angular/material/sort';
import {ActivatedRoute, Router} from '@angular/router';
import {AuthenticationService} from '../_services/authentication/authentication-service';
import {EmailLog} from '../_models/email_log';
import {User} from '../_models/user';

@Component({
  selector: 'app-email-log-admin',
  templateUrl: './email-log-admin.component.html',
  styleUrls: ['./email-log-admin.component.scss']
})
export class EmailLogAdminComponent implements OnInit {
  @ViewChild(MatSort, {static: true}) sort: MatSort;
  currentUser: User;
  dataSource: MatTableDataSource<EmailLog>;
  displayedColumns: string[] = ['id', 'user_id', 'type', 'viewed', 'date_viewed', 'last_updated'];
  loading = true;

  constructor(
    private api: ApiService,
    private route: ActivatedRoute,
    private authenticationService: AuthenticationService,
  ) {
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
  }

  ngOnInit() {
    this.api.getAllEmailLog().subscribe(log => {
      this.dataSource = new MatTableDataSource<EmailLog>(log);
      this.dataSource.sort = this.sort;
      this.loading = false;
    });
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }
}
