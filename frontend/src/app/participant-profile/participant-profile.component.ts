import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { Participant } from '../participant';
import { UserParticipant } from '../user-participant';

@Component({
  selector: 'app-participant-profile',
  templateUrl: './participant-profile.component.html',
  styleUrls: ['./participant-profile.component.scss']
})
export class ParticipantProfileComponent implements OnInit {
  @Input() userParticipant: UserParticipant;
  participant: Participant;
  dummyImgUrl: string;
  percentComplete: number;
  numStudies: number;

  constructor(
    private router: Router
  ) {
    this.dummyImgUrl = this.randomImgUrl();
  }

  ngOnInit() {
    this.participant = new Participant(this.userParticipant.participant);

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

  goEditEnroll($event) {
    if (this.userParticipant.relationship == 'self') {
      $event.preventDefault();
      this.router.navigate(['participant', this.participant.id, 'self_intake']);
    } else if (this.userParticipant.relationship == 'dependent') {
      $event.preventDefault();
      this.router.navigate(['participant', this.participant.id, 'dependent_intake']);
    } else {
      $event.preventDefault();
      this.router.navigate(['participant', this.participant.id, 'guardian_intake']);
    }
  }
}
