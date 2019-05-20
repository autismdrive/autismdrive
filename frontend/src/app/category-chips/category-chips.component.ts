import { Component, OnInit, Input } from '@angular/core';
import { StudyCategory } from '../_models/study_category';
import { ResourceCategory } from '../_models/resource_category';

@Component({
  selector: 'app-category-chips',
  templateUrl: './category-chips.component.html',
  styleUrls: ['./category-chips.component.scss']
})
export class CategoryChipsComponent implements OnInit {
  @Input() categories: StudyCategory[] | ResourceCategory[];

  constructor() {

  }

  ngOnInit() {
    console.log('this.categories', this.categories);
  }

}
