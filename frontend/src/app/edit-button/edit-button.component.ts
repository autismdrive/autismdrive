import {Component, Input} from '@angular/core';
import {Router} from '@angular/router';
import {User} from '../_models/user';

@Component({
  selector: 'app-edit-button',
  templateUrl: './edit-button.component.html',
  styleUrls: ['./edit-button.component.scss'],
})
export class EditButtonComponent {
  @Input() currentUser: User;
  @Input() editLabel: string;
  @Input() editLink: string;

  constructor(private router: Router) {}

  openEdit() {
    this.router.navigateByUrl(this.editLink);
  }
}
