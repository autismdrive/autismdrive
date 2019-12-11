import { Component, OnInit } from '@angular/core';
import { ApiService } from '../_services/api/api.service';
import { UserParticipantList } from '../_models/user_participant_list';
import { Participant } from '../_models/participant';

@Component({
  selector: 'app-participant-admin',
  templateUrl: './participant-admin.component.html',
  styleUrls: ['./participant-admin.component.scss']
})
export class ParticipantAdminComponent implements OnInit {
  userParticipantList: UserParticipantList;
  participantDataSource: Participant[];
  displayedColumns: string[] = ['id', 'name', 'user_id', 'relationship', 'percent_complete', 'has_consented', 'last_updated'];
  loading: boolean = true;

  constructor(
    private api: ApiService,
  ) { }

  ngOnInit() {
    this.api.getUserParticipantList().subscribe( upl => {
      this.userParticipantList = upl;
      this.participantDataSource = upl.all_participants[0];
      this.loading = false;
    })
  }

}
