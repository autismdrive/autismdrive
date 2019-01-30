import { Component, OnInit, Input } from '@angular/core';
import { Participant } from '../participant';

@Component({
  selector: 'app-participant-profile',
  templateUrl: './participant-profile.component.html',
  styleUrls: ['./participant-profile.component.scss']
})
export class ParticipantProfileComponent implements OnInit {
  @Input() participant: Participant;

  constructor() { }

  ngOnInit() {
  }

}
