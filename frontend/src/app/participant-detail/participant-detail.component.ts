import {Component, Input, OnInit} from '@angular/core';
import {MatTableDataSource} from '@angular/material/table';
import {Participant} from '@models/participant';
import {StepLog} from '@models/step_log';
import {ApiService} from '@services/api/api.service';

@Component({
  selector: 'app-participant-detail',
  templateUrl: './participant-detail.component.html',
  styleUrls: ['./participant-detail.component.scss'],
})
export class ParticipantDetailComponent implements OnInit {
  @Input() participant: Participant;

  dataSource: MatTableDataSource<StepLog>;
  displayedColumns: string[] = [
    'id',
    'questionnaire_name',
    'questionnaire_id',
    'flow',
    'participant_id',
    'user_id',
    'date_completed',
    'time_on_task_ms',
  ];

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.getParticipantStepLog(this.participant).subscribe(log => {
      this.participant.step_log = log;
      this.dataSource = new MatTableDataSource<StepLog>(log);
    });
  }
}
