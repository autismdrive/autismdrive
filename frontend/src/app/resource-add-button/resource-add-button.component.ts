import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { User } from '../_models/user';

@Component({
  selector: 'app-resource-add-button',
  templateUrl: './resource-add-button.component.html',
  styleUrls: ['./resource-add-button.component.scss']
})
export class ResourceAddButtonComponent implements OnInit {
  @Input() currentUser: User;

  constructor(
    private router: Router
  ) { }

  ngOnInit() {
  }

  openAdd() {
    this.router.navigateByUrl(`resources/add`);
  }
}
