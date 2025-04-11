import {CommonModule, DatePipe, UpperCasePipe} from '@angular/common';
import {ChangeDetectionStrategy, Component, effect} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatLineModule} from '@angular/material/core';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatSelectModule} from '@angular/material/select';
import {MatTableDataSource, MatTableModule} from '@angular/material/table';
import {ActivatedRoute} from '@angular/router';
import {ParticipantDetailComponent} from '@app/participant-detail/participant-detail.component';
import {AdminNote} from '@models/admin_note';
import {EmailLog} from '@models/email_log';
import {ResourceChangeLog} from '@models/resource_change_log';
import {User} from '@models/user';
import {FlexModule} from '@ngbracket/ngx-layout';
import {ApiService} from '@services/api/api.service';
import {AuthenticationService} from '@services/authentication/authentication-service';

@Component({
  standalone: true,
  selector: 'app-user-admin-details',
  templateUrl: './user-admin-details.component.html',
  styleUrls: ['./user-admin-details.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [
    CommonModule,
    DatePipe,
    FlexModule,
    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatLineModule,
    MatSelectModule,
    MatTableModule,
    ParticipantDetailComponent,
    UpperCasePipe,
  ],
})
export class UserAdminDetailsComponent {
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
    effect(() => {
      this.currentUser = this.authenticationService.currentUser();
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
              this.api.getParticipantStepLog(pi).subscribe(log => {
                pi.step_log = log;
              });
            });
          });
        }
      });
    });
  }

  exportUserData() {
    this.api.exportUserQuestionnaire(this.user.id.toString()).subscribe(response => {
      const filename = response.headers.get('x-filename');
      const blob = new Blob([response.body], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      });

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
