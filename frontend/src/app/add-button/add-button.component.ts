import {Component, Input} from '@angular/core';
import {Router} from '@angular/router';
import {User} from '@models/user';

@Component({
  selector: 'app-add-button',
  templateUrl: './add-button.component.html',
  styleUrls: ['./add-button.component.scss'],
})
export class AddButtonComponent {
  @Input() currentUser: User;
  @Input() addLink: string;
  @Input() addLabel: string;

  constructor(private router: Router) {}

  openAdd() {
    this.router.navigateByUrl(this.addLink);
  }
}
