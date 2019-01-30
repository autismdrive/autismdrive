import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { User } from '../user';
import { Participant } from '../participant';


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
  participants: Participant[] = [
    {
      first_name: 'Firstname',
      nickname: '',
      last_name: 'Lastname',
      relationship: 'self',
      percent_complete: 20,
      num_studies_enrolled: 0,
      avatar_img_url: 'https://pbs.twimg.com/profile_images/477556215401025537/zH_q0-_s.png'
    },
    {
      first_name: 'Childname',
      nickname: 'Nickname',
      last_name: 'Lastname',
      relationship: 'dependent',
      percent_complete: 100,
      num_studies_enrolled: 3,
      avatar_img_url: 'https://pbs.twimg.com/profile_images/493362921817120770/23Hg2d2k.jpeg'
    },
  ];

  constructor(
    private api: ApiService
  ) {

    this.api.getSession().subscribe(user => {
      this.user = user;
      this.loading = false;
    }, error1 => {
      this.user = null;
      this.loading = false;
    });
  }

  ngOnInit() {
  }



}
