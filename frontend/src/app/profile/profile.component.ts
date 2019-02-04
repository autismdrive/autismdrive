import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { User } from '../user';
import { Participant } from '../participant';
import { UserParticipant } from '../user-participant';


@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  user: User;
  stepName: string;
  activeStep = 0;
  loading = true;
  userParticipants: UserParticipant[];
  currentId: number;
  firstNames = [
    'Atreyu',
    'Moon Child',
    'Bastian',
    'Falkor',
    'Engywook',
    'Urgl'
  ];
  lastNames = [
    'Artax',
    'Gmorg',
    'Rockbiter'
  ];

  constructor(
    private api: ApiService
  ) {
    this.currentId = Math.floor(Math.random() * 99999999) + 999;


    console.log('Calling getSession from ProfileComponent constructor');
    this.api.getSession().subscribe(user => {
      console.log('ProfileComponent constructor > getSession callback user', user);

      this.user = user;
      this.userParticipants = user.participants;
      this.loading = false;
    }, error1 => {
      console.error(error1);
      this.user = null;
      this.loading = false;
    });
  }

  ngOnInit() {
  }

  addParticipant(relationship: string) {
    this.loading = true;
    const name = this.randomName();
    const options: Participant = {
      id: ++this.currentId,
      last_updated: new Date(),
      first_name: name.first,
      last_name: name.last,
      users: []
    };

    this.api.addParticipant(relationship, options).subscribe(participant => {
      console.log('new participant', participant);

      this.api.getSession().subscribe(updatedUser => {
        this.user = updatedUser;
        this.userParticipants = updatedUser.participants;
        this.loading = false;
      });
    });
  }

  randomName() {
    const firstIndex = Math.floor(Math.random() * this.firstNames.length);
    const lastIndex = Math.floor(Math.random() * this.lastNames.length);

    return {
      first: this.firstNames[firstIndex],
      last: this.lastNames[lastIndex]
    };
  }

  isAlreadyEnrolled(relationship: string): boolean {
    for (const up of this.user.participants) {
      if (up.relationship === relationship) { return true; }
    }

    return false;
  }

}
