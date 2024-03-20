import {Component, OnInit, ViewChild} from '@angular/core';
import {MatSort} from '@angular/material/sort';
import {MatTableDataSource} from '@angular/material/table';
import {ActivatedRoute} from '@angular/router';
import {EmailLog} from '../_models/email_log';
import {User} from '../_models/user';
import {ApiService} from '../_services/api/api.service';
import {AuthenticationService} from '../_services/authentication/authentication-service';

@Component({
  selector: 'app-email-log-admin',
  templateUrl: './email-log-admin.component.html',
  styleUrls: ['./email-log-admin.component.scss'],
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
    this.authenticationService.currentUser.subscribe(x => (this.currentUser = x));
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
