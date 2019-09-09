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

}
