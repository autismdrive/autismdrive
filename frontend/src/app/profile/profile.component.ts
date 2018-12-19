import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { User } from '../user';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  session: User;

  constructor(
    private api: ApiService
  ) { }

  ngOnInit() {
    this.api.getSession().subscribe(user => {
      console.log(user);
      this.session = user;
    }, error1 => {
      this.session = null;
    });
  }

}
