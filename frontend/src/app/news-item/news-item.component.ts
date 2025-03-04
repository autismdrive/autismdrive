import {NgClass, NgOptimizedImage} from '@angular/common';
import {Component, Input, OnInit} from '@angular/core';
import {RouterModule} from '@angular/router';
import {DetailsLinkComponent} from '@app/details-link/details-link.component';
import {NewsItem} from '@models/news-item';

@Component({
  standalone: true,
  selector: 'app-news-item',
  templateUrl: './news-item.component.html',
  styleUrls: ['./news-item.component.scss'],
  imports: [NgClass, RouterModule, NgOptimizedImage, DetailsLinkComponent],
})
export class NewsItemComponent implements OnInit {
  @Input() item: NewsItem;
  @Input() index: number;

  constructor() {}

  ngOnInit() {
    if (!this.item.label) {
      this.item.label = 'Details';
    }
  }

  isEven(i: number) {
    return i % 2 === 0;
  }
}
