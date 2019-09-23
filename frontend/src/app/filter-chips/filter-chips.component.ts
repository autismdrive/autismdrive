import { Component, OnInit, Input } from '@angular/core';
import { StudyCategory } from '../_models/study_category';
import { ResourceCategory } from '../_models/resource_category';
import {AgeRange} from '../_models/hit_type';

@Component({
  selector: 'app-filter-chips',
  templateUrl: './filter-chips.component.html',
  styleUrls: ['./filter-chips.component.scss']
})
export class FilterChipsComponent implements OnInit {
  @Input() categories: StudyCategory[] | ResourceCategory[] = [];
  @Input() ages: string[] = [];

  ageLabels = AgeRange.labels;

  constructor() {

  }

  ngOnInit() {
  }

}
