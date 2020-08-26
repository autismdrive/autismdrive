import {Component, Input, OnInit} from '@angular/core';
import {Resource} from '../_models/resource';
import {Router} from '@angular/router';
import {MatDialog} from '@angular/material/dialog';
import {EventRegistrationFormComponent} from '../event-registration-form/event-registration-form.component';

@Component({
  selector: 'app-event-registration',
  templateUrl: './event-registration.component.html',
  styleUrls: ['./event-registration.component.scss']
})
export class EventRegistrationComponent implements OnInit {
  @Input() resource: Resource;
  @Input() currentUser = false;

  constructor(
    private router: Router,
    public dialog: MatDialog
  ) { }

  ngOnInit() {
  }

  goLogin() {
    this.router.navigate(['/login'], {queryParams: {returnUrl: this.router.url}});
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(EventRegistrationFormComponent, {
      width: `${window.innerWidth}px`,
      data: {
        'registered': false,
        'title': 'Register for ' + this.resource.title,
        'event_id': this.resource.id
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.currentUser = true;
      }
    });
  }
}
