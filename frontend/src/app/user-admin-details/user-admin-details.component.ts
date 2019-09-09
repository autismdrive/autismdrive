import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Participant } from '../_models/participant';
import { User } from '../_models/user';
import { ApiService } from '../_services/api/api.service';
import { MatTableDataSource } from '@angular/material';
import { EmailLog } from '../_models/email_log';

@Component({
  selector: 'app-user-admin-details',
  templateUrl: './user-admin-details.component.html',
  styleUrls: ['./user-admin-details.component.scss']
})
export class UserAdminDetailsComponent implements OnInit {
  user: User;
  dataSource: MatTableDataSource<EmailLog>;
  displayedColumns:  string[] = ['id', 'user_id', 'type', 'tracking_code', 'viewed', 'date_viewed'];

  constructor(
    private api: ApiService, private route: ActivatedRoute
  ) {
    this.route.params.subscribe(params => {
      const userId = params.userId ? parseInt(params.userId, 10) : null;

      if (isFinite(userId)) {
        this.api.getUser(userId).subscribe(user => {
          this.user = user;

          this.api.getUserEmailLog(this.user).subscribe( log => {
            this.user.email_log = log;
            this.dataSource = new MatTableDataSource<EmailLog>(log);
          });

          for (let pi in this.user.participants) {
              let participant = new Participant(this.user.participants[pi]);
              this.api.getFlow(participant.getFlowName(), participant.id)
              .subscribe(f => {
                participant.percent_complete = f.percentComplete();
              });
              this.api.getParticipantStepLog(participant).subscribe( log => {
                participant.step_log = log;
              });
              this.user.participants[pi] = participant;
          }
        });
      }
    });
  }

  ngOnInit() {
  }

  exportUserData() {
    console.log('clicking the button for export user data');
    this.api.exportUserQuestionnaire(this.user.id.toString()).subscribe( response => {
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
}
