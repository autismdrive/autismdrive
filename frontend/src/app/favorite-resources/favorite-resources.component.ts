import {CommonModule} from '@angular/common';
import {Component, Input} from '@angular/core';
import {MatButtonModule} from '@angular/material/button';
import {MatLine} from '@angular/material/core';
import {MatListModule} from '@angular/material/list';
import {RouterModule} from '@angular/router';
import {Resource} from '@models/resource';

@Component({
  standalone: true,
  selector: 'app-favorite-resources',
  templateUrl: './favorite-resources.component.html',
  styleUrls: ['./favorite-resources.component.scss'],
  imports: [MatListModule, CommonModule, MatLine, RouterModule, MatButtonModule],
})
export class FavoriteResourcesComponent {
  @Input() favoriteResources: Resource[];

  constructor() {}
}
