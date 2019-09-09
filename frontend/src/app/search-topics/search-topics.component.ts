import {Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges} from '@angular/core';
import {Query} from '../_models/query';
import {Category} from '../_models/category';

@Component({
  selector: 'app-search-topics',
  templateUrl: './search-topics.component.html',
  styleUrls: ['./search-topics.component.scss']
})
export class SearchTopicsComponent implements OnInit, OnChanges {

  @Input()
  category: Category;

  @Output()
  catagorySelected = new EventEmitter<Category>();

  changeCount = 0;

  example_data = {
        'id': 12, 'name': 'Toys', level: 3,
        'parent': {
          'id': 10, 'name': 'Dog', level: 2,
          'parent': {
            'id': 10, 'name': 'Animals', level: 1
          }
        },
        'children': [
          {'id': 25, 'name': 'Fetch Toys', level: 4, 'hit_count': 12},
          {'id': 25, 'name': 'Chew Toys', level: 4, 'hit_count': 10},
          {'id': 25, 'name': 'Plush Toys', level: 4, 'hit_count': 7}
        ]
  };

  constructor() { }

  ngOnInit() {
  }

  selectCategory(cat: Category) {
    this.catagorySelected.emit(cat);
  }

  parentList(current: Category = this.category, parents: any[] = []): any[] {
    if (current.parent) {
      parents.unshift(current.parent);
      return this.parentList(current.parent, parents);
    } else {
      return parents;
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.changeCount++;
  }

}
