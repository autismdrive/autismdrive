import { Component, OnInit, Input } from '@angular/core';
import { StudyCategory } from '../_models/study_category';
import { ResourceCategory } from '../_models/resource_category';
import { TrainingCategory } from '../_models/training_category';

@Component({
  selector: 'app-category-chips',
  templateUrl: './category-chips.component.html',
  styleUrls: ['./category-chips.component.scss']
})
export class CategoryChipsComponent implements OnInit {
  @Input() categories: StudyCategory[] | ResourceCategory[] | TrainingCategory[];

  constructor() { }

  ngOnInit() {
  }

}
