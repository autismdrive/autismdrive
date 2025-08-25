import {CommonModule} from '@angular/common';
import {Component} from '@angular/core';
import {MatTabsModule} from '@angular/material/tabs';
import {RouterModule} from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-admin-home',
  templateUrl: './admin-home.component.html',
  styleUrls: ['./admin-home.component.scss'],
  imports: [RouterModule, MatTabsModule, CommonModule],
})
export class AdminHomeComponent {
  navLinks = [
    {path: '/admin/data-admin', label: 'Data Admin', id: 'data-admin'},
    {path: '/admin/user-admin', label: 'User Admin', id: 'user-admin'},
    {path: '/admin/participant-admin', label: 'Participant Admin', id: 'participant-admin'},
    {path: '/admin/taxonomy-admin', label: 'Taxonomy Admin', id: 'taxonomy-admin'},
    {path: '/admin/import-export-status', label: 'Import/Export Status', id: 'import-export-status'},
    {path: '/admin/email-log', label: 'Email Log', id: 'email-log'},
    // { path: '/admin/skillstar-admin', label: 'SkillSTAR Admin', id: 'skillstar-admin'  },
  ];

  constructor() {}
}
