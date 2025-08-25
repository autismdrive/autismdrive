import {Component} from '@angular/core';
import {MatCheckboxModule} from '@angular/material/checkbox';

@Component({
  standalone: true,
  selector: 'app-filters',
  templateUrl: './filters.component.html',
  styleUrls: ['./filters.component.scss'],
  imports: [MatCheckboxModule],
})
export class FiltersComponent {
  constructor() {}
}
