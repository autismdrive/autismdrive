import {Component, Input} from '@angular/core';
import {Resource} from '@models/resource';

@Component({
  selector: 'app-favorite-resources',
  templateUrl: './favorite-resources.component.html',
  styleUrls: ['./favorite-resources.component.scss'],
})
export class FavoriteResourcesComponent {
  @Input() favoriteResources: Resource[];

  constructor() {}
}
