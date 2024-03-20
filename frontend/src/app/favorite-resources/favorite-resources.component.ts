import {Component, Input, OnInit} from '@angular/core';
import {Resource} from '../_models/resource';

@Component({
  selector: 'app-favorite-resources',
  templateUrl: './favorite-resources.component.html',
  styleUrls: ['./favorite-resources.component.scss'],
})
export class FavoriteResourcesComponent implements OnInit {
  @Input() favoriteResources: Resource[];

  constructor() {}

  ngOnInit() {}
}
