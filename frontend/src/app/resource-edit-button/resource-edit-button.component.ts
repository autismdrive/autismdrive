import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Resource } from '../_models/resource';
import { User } from '../_models/user';

@Component({
  selector: 'app-resource-edit-button',
  templateUrl: './resource-edit-button.component.html',
  styleUrls: ['./resource-edit-button.component.scss']
})
export class ResourceEditButtonComponent implements OnInit {
  @Input() resource: Resource;
  @Input() currentUser: User;

  constructor(
    private router: Router
  ) { }

  ngOnInit() {
  }

  openEdit() {
    this.router.navigateByUrl(`resource/${this.resource.id}/edit`);
  }
}
