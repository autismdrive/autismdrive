import {NgIf} from '@angular/common';
import {Component, Input} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatDialog} from '@angular/material/dialog';
import {Router} from '@angular/router';
import {Resource} from '@models/resource';
import {FlexModule} from '@ngbracket/ngx-layout';
import {EventRegistrationFormComponent} from '../event-registration-form/event-registration-form.component';

@Component({
  standalone: true,
  selector: 'app-event-registration',
  templateUrl: './event-registration.component.html',
  styleUrls: ['./event-registration.component.scss'],
  imports: [FlexModule, MatButtonModule, NgIf],
})
export class EventRegistrationComponent {
  @Input() resource: Resource;
  @Input() hasCurrentUser = false;

  constructor(
    private router: Router,
    public dialog: MatDialog,
  ) {}

  goLogin() {
    this.router.navigate(['/login'], {queryParams: {returnUrl: this.router.url}});
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(EventRegistrationFormComponent, {
      data: {
        registered: false,
        title: 'Register for ' + this.resource.title,
        event_id: this.resource.id,
      },
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.hasCurrentUser = true;
      }
    });
  }
}
