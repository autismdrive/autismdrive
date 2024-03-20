import {Component, Input, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {User} from '../_models/user';

@Component({
  selector: 'app-add-button',
  templateUrl: './add-button.component.html',
  styleUrls: ['./add-button.component.scss'],
})
export class AddButtonComponent implements OnInit {
  @Input() currentUser: User;
  @Input() addLink: string;
  @Input() addLabel: string;

  constructor(private router: Router) {}

  ngOnInit() {}

  openAdd() {
    this.router.navigateByUrl(this.addLink);
  }
}
