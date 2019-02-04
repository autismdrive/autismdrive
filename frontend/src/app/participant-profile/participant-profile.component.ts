import { Component, OnInit, Input } from '@angular/core';
import { Participant } from '../participant';
import { UserParticipant } from '../user-participant';

@Component({
  selector: 'app-participant-profile',
  templateUrl: './participant-profile.component.html',
  styleUrls: ['./participant-profile.component.scss']
})
export class ParticipantProfileComponent implements OnInit {
  @Input() userParticipant: UserParticipant;
  dummyImgUrl: string;
  percentComplete: number;
  numStudies: number;

  constructor() {
    this.dummyImgUrl = this.randomImgUrl();
  }

  ngOnInit() {
    if (isFinite(this.userParticipant.participant.percent_complete)) {
      this.percentComplete = this.userParticipant.participant.percent_complete;
    } else {
      this.percentComplete = Math.ceil(Math.random() * 5) * 20;
    }

    if (isFinite(this.userParticipant.participant.num_studies_enrolled)) {
      this.numStudies = this.userParticipant.participant.num_studies_enrolled;
    } else {
      this.numStudies = Math.floor(Math.random() * 5) + 1;
    }
  }

  randomImgUrl() {
    const gender = Math.random() > 0.5 ? 'men' : 'women';
    const id = Math.floor(Math.random() * 100);
    return `https://randomuser.me/api/portraits/med/${gender}/${id}.jpg`;
  }
}
