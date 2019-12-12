import { Component, OnInit, ViewChild } from '@angular/core';
import { ApiService } from '../_services/api/api.service';
import { Participant } from '../_models/participant';
import { UserParticipantList } from '../_models/user_participant_list';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material';

@Component({
  selector: 'app-participant-admin',
  templateUrl: './participant-admin.component.html',
  styleUrls: ['./participant-admin.component.scss']
})
export class ParticipantAdminComponent implements OnInit {
  @ViewChild(MatSort, {static: false}) sort: MatSort;
  userParticipantList: UserParticipantList;
  participantDataSource: MatTableDataSource<Participant>;
  displayedColumns: string[] = ['id', 'name', 'user_id', 'relationship', 'percent_complete', 'has_consented', 'last_updated'];
  loading: boolean = true;

  constructor(
    private api: ApiService,
  ) { }

  ngOnInit() {
    this.api.getUserParticipantList().subscribe( upl => {
      this.userParticipantList = upl;
      this.participantDataSource = new MatTableDataSource(upl.all_participants[0]);
      this.participantDataSource.sort = this.sort;
      this.loading = false;
    })
  }

}
