import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { Participant } from '../participant';
import { User } from '../user';

@Component({
  selector: 'app-participant-profile',
  templateUrl: './participant-profile.component.html',
  styleUrls: ['./participant-profile.component.scss']
})
export class ParticipantProfileComponent implements OnInit {
  @Input() participant: Participant;
  @Input() user: User;
  dummyImgUrl: string;
  percentComplete: number;
  numStudies: number;

  constructor(private router: Router) {
    this.dummyImgUrl = this.randomImgUrl();
  }

  ngOnInit() {
    if (isFinite(this.participant.percent_complete)) {
      this.percentComplete = this.participant.percent_complete;
    } else {
      this.percentComplete = Math.ceil(Math.random() * 5) * 20;
    }

    if (isFinite(this.participant.num_studies_enrolled)) {
      this.numStudies = this.participant.num_studies_enrolled;
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
    if (this.participant.relationship === User.SELF_PARTICIPANT) {
      $event.preventDefault();
      this.router.navigate(['participant', this.participant.id, 'self_intake']);
    } else if (this.participant.relationship === User.DEPENDENT) {
      $event.preventDefault();
      this.router.navigate(['participant', this.participant.id, 'dependent_intake']);
    } else {
      $event.preventDefault();
      this.router.navigate(['participant', this.participant.id, 'guardian_intake']);
    }
  }
}
