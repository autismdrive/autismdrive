import {CommonModule, DatePipe} from '@angular/common';
import {ChangeDetectionStrategy, Component, effect, OnInit, ViewChild} from '@angular/core';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import {MatSort, MatSortModule} from '@angular/material/sort';
import {MatTableDataSource, MatTableModule} from '@angular/material/table';
import {ActivatedRoute} from '@angular/router';
import {EmailLog} from '@models/email_log';
import {User} from '@models/user';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';

@Component({
  standalone: true,
  selector: 'app-email-log-admin',
  templateUrl: './email-log-admin.component.html',
  styleUrls: ['./email-log-admin.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [
    CommonModule,
    DatePipe,
    MatFormFieldModule,
    MatInputModule,
    MatProgressSpinnerModule,
    MatSortModule,
    MatTableModule,
  ],
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
    effect(() => {
      this.currentUser = this.authenticationService.currentUser();
    });
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
