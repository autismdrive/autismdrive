import {Component, Input, OnInit} from '@angular/core';
import {User} from '../_models/user';
import {Router} from '@angular/router';

@Component({
  selector: 'app-add-button',
  templateUrl: './add-button.component.html',
  styleUrls: ['./add-button.component.scss']
})
export class AddButtonComponent implements OnInit {
  @Input() currentUser: User;
  @Input() addLink: string;
  @Input() addLabel: string;

  constructor(
    private router: Router
  ) { }

  ngOnInit() {
    console.log('this is the addLabel', this.addLabel);
    console.log('this is the addLink', this.addLink);
    console.log('this is the currentUser', this.currentUser);
  }

  openAdd() {
    this.router.navigateByUrl(this.addLink);
  }
}
