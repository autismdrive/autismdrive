import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { Participant } from '../participant';
import { User } from '../user';
import { Flow } from '../flow';
import { ApiService } from '../services/api/api.service';

@Component({
  selector: 'app-participant-profile',
  templateUrl: './participant-profile.component.html',
  styleUrls: ['./participant-profile.component.scss']
})
export class ParticipantProfileComponent implements OnInit {
  @Input() participant: Participant;
  @Input() user: User;
  flow: Flow;
  dummyImgUrl: string;
  percentComplete: number;
  numStudies: number;

  constructor(
    private api: ApiService,
    private router: Router
  ) {
    this.dummyImgUrl = this.randomImgUrl();
  }

  ngOnInit() {
    if (this.participant) {
      this.api
        .getFlow(this.participant.getFlowName(), this.participant.id)
        .subscribe(f => {
          this.flow = new Flow(f);
          console.log('this.flow', this.flow);
          this.percentComplete = this.flow.percentComplete();
          console.log('this.percentComplete', this.percentComplete);
        });
    }

    if (isFinite(this.participant.num_studies_enrolled)) {
      this.numStudies = this.participant.num_studies_enrolled;
    } else {
      this.numStudies = 0;
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
