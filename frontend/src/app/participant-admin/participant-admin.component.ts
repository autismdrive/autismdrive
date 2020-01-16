import {Component, OnInit, ViewChild} from '@angular/core';
import {MatTableDataSource} from '@angular/material';
import {MatSort} from '@angular/material/sort';
import {Participant} from '../_models/participant';
import {ParticipantAdminList} from '../_models/participant_admin_list';
import {ApiService} from '../_services/api/api.service';

@Component({
  selector: 'app-participant-admin',
  templateUrl: './participant-admin.component.html',
  styleUrls: ['./participant-admin.component.scss']
})
export class ParticipantAdminComponent implements OnInit {
  @ViewChild(MatSort, {static: true}) sort: MatSort;
  userParticipantList: ParticipantAdminList;
  participantDataSource: MatTableDataSource<Participant>;
  displayedColumns: string[] = ['id', 'name', 'user_id', 'relationship', 'percent_complete', 'has_consented', 'last_updated'];
  loading = true;

  constructor(
    private api: ApiService,
  ) {
  }

  ngOnInit() {
    this.api.getParticipantAdminList().subscribe(pal => {
      this.userParticipantList = pal;
      this.participantDataSource = new MatTableDataSource(pal.all_participants[0]);
      this.participantDataSource.sort = this.sort;
      this.loading = false;
    });
  }

}