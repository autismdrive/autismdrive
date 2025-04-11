import {CommonModule} from '@angular/common';
import {Component, Input} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatTooltip} from '@angular/material/tooltip';
import {RouterModule} from '@angular/router';
import {User} from '@models/user';

@Component({
  standalone: true,
  selector: 'app-add-button',
  templateUrl: './add-button.component.html',
  styleUrls: ['./add-button.component.scss'],
  imports: [CommonModule, MatButtonModule, MatTooltip, RouterModule],
})
export class AddButtonComponent {
  @Input() currentUser: User;
  @Input() addLink: string;
  @Input() addLabel: string;

  constructor() {}
}
