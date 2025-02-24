import {NgIf, PercentPipe} from '@angular/common';
import {Component, OnInit, ViewChild} from '@angular/core';
import {MatCardModule} from '@angular/material/card';
import {MatDivider, MatDividerModule} from '@angular/material/divider';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInput, MatInputModule} from '@angular/material/input';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import {MatSort, MatSortModule} from '@angular/material/sort';
import {MatTableDataSource, MatTableModule} from '@angular/material/table';
import {Participant} from '@models/participant';
import {ParticipantAdminList} from '@models/participant_admin_list';
import {FlexModule} from '@ngbracket/ngx-layout';
import {ApiService} from '@services/api/api.service';

@Component({
  standalone: true,
  selector: 'app-participant-admin',
  templateUrl: './participant-admin.component.html',
  styleUrls: ['./participant-admin.component.scss'],
  imports: [
    FlexModule,
    MatProgressSpinnerModule,
    MatCardModule,
    MatDividerModule,
    MatFormFieldModule,
    MatTableModule,
    MatSortModule,
    MatInputModule,
    NgIf,
    PercentPipe,
  ],
})
export class ParticipantAdminComponent implements OnInit {
  @ViewChild(MatSort, {static: true}) sort: MatSort;
  userParticipantList: ParticipantAdminList;
  participantDataSource = new MatTableDataSource<Participant>([]);
  displayedColumns: string[] = [
    'id',
    'name',
    'user_id',
    'relationship',
    'percent_complete',
    'has_consented',
    'last_updated',
  ];
  loading = true;

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.getParticipantAdminList().subscribe(pal => {
      this.userParticipantList = pal;
      this.participantDataSource.data = pal.all_participants;
      this.participantDataSource.sort = this.sort;
      this.loading = false;
    });
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.participantDataSource.filter = filterValue.trim().toLowerCase();
  }
}
