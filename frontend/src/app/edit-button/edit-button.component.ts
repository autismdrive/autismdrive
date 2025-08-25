import {CommonModule} from '@angular/common';
import {Component, Input} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import {MatTooltipModule} from '@angular/material/tooltip';
import {RouterModule} from '@angular/router';
import {User} from '@models/user';

@Component({
  standalone: true,
  selector: 'app-edit-button',
  templateUrl: './edit-button.component.html',
  styleUrls: ['./edit-button.component.scss'],
  imports: [CommonModule, MatButtonModule, MatIconModule, MatTooltipModule, RouterModule],
})
export class EditButtonComponent {
  @Input() currentUser: User;
  @Input() editLabel: string;
  @Input() editLink: string;

  constructor() {}

  shouldDisplayButton() {
    return (
      this.currentUser &&
      (this.currentUser.permissions.includes('edit_resource') || this.currentUser.permissions.includes('edit_study'))
    );
  }
}
