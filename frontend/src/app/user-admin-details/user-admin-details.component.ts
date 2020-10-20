import {Component, OnInit} from '@angular/core';
import {MatTableDataSource} from '@angular/material/table';
import {ActivatedRoute} from '@angular/router';
import {AdminNote} from '../_models/admin_note';
import {EmailLog} from '../_models/email_log';
import {ResourceChangeLog} from '../_models/resource_change_log';
import {User} from '../_models/user';
import {ApiService} from '../_services/api/api.service';
import {AuthenticationService} from '../_services/api/authentication-service';

@Component({
  selector: 'app-user-admin-details',
  templateUrl: './user-admin-details.component.html',
  styleUrls: ['./user-admin-details.component.scss']
})
export class UserAdminDetailsComponent implements OnInit {
  user: User;
  currentUser: User;
  dataSource: MatTableDataSource<EmailLog>;
  displayedColumns: string[] = ['id', 'user_id', 'type', 'tracking_code', 'viewed', 'date_viewed'];
  adminNotes: AdminNote[];
  resourceChangeLog: ResourceChangeLog[];
  roleSelected: string;

  constructor(
    private api: ApiService,
    private route: ActivatedRoute,
    private authenticationService: AuthenticationService,
  ) {
    this.authenticationService.currentUser.subscribe(x => this.currentUser = x);
    this.route.params.subscribe(params => {
      const userId = params.userId ? parseInt(params.userId, 10) : null;

      if (isFinite(userId)) {
        this.api.getUser(userId).subscribe(user => {
          this.user = user;
          this.roleSelected = user.role;

          this.api.getUserEmailLog(this.user).subscribe(log => {
            this.user.email_log = log;
            this.dataSource = new MatTableDataSource<EmailLog>(log);
          });

          this.api.getUserAdminNotes(this.user.id).subscribe(notes => {
            this.adminNotes = notes;
          });

          this.api.getUserResourceChangeLog(this.user.id).subscribe(log => {
            this.resourceChangeLog = log;
          });

          this.user.participants.forEach(pi => {
            this.api
              .getParticipantStepLog(pi)
              .subscribe(log => {
                pi.step_log = log;
              });
          });
        });
      }
    });
  }

  ngOnInit() {
  }

  exportUserData() {
    console.log('clicking the button for export user data');
    this.api.exportUserQuestionnaire(this.user.id.toString()).subscribe(response => {
      console.log('data', response);
      const filename = response.headers.get('x-filename');
      const blob = new Blob([response.body], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});

      const url = URL.createObjectURL(blob);
      const a: HTMLAnchorElement = document.createElement('a') as HTMLAnchorElement;

      a.href = url;
      a.download = filename;
      window.document.body.appendChild(a);
      a.click();
      window.document.body.removeChild(a);
      URL.revokeObjectURL(url);
    });
  }

  saveSelection() {
    this.user.role = this.roleSelected;
    this.api.updateUser(this.user).subscribe();
  }

}
