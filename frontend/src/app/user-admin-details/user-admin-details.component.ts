import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import { User } from '../_models/user';
import {ApiService} from '../_services/api/api.service';

@Component({
  selector: 'app-user-admin-details',
  templateUrl: './user-admin-details.component.html',
  styleUrls: ['./user-admin-details.component.scss']
})
export class UserAdminDetailsComponent implements OnInit {
  user: User;

  constructor(private api: ApiService, private route: ActivatedRoute) {
    this.route.params.subscribe(params => {
      const userId = params.userId ? parseInt(params.userId, 10) : null;

      if (isFinite(userId)) {
        this.api.getUser(userId).subscribe(user => {
          this.user = user;
        });
      }
    });
  }
  ngOnInit() {
  }

}
