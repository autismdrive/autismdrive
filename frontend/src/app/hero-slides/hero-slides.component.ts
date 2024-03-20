import {Component, Input, OnInit} from '@angular/core';
import {NewsItem} from '../_models/news-item';
import {IntervalService} from '../_services/interval/interval.service';

@Component({
  selector: 'app-hero-slides',
  templateUrl: './hero-slides.component.html',
  styleUrls: ['./hero-slides.component.scss'],
})
export class HeroSlidesComponent implements OnInit {
  @Input() slides: NewsItem[];
  activeIndex = 0;
  delayMs = 5000;

  constructor(private intervalService: IntervalService) {
    intervalService.setInterval(() => {
      this._incrementActiveIndex();
    }, this.delayMs);
  }

  ngOnInit() {}

  _incrementActiveIndex() {
    if (this.activeIndex < this.slides.length - 1) {
      this.activeIndex++;
    } else {
      this.activeIndex = 0;
    }
  }

  setActiveSlide(slideIndex: number) {
    this.activeIndex = slideIndex;

    // Reset the timer
    this.intervalService.clearInterval();
    this.intervalService.setInterval(() => {
      this._incrementActiveIndex();
    }, this.delayMs);
  }

  activeClass(slideIndex: number): string {
    if (slideIndex === this.activeIndex) {
      return 'active';
    } else {
      if (this.activeIndex === this.slides.length - 1) {
        // Last slide
        // On last slide, first slide is next
        return slideIndex === 0 ? 'next' : 'prev';
      } else if (this.activeIndex === 0) {
        // First slide
        // On first slide, last slide is prev
        return slideIndex === this.slides.length - 1 ? 'prev' : 'next';
      } else {
        // Middle slide
        return slideIndex < this.activeIndex ? 'prev' : 'next';
      }
    }
  }
}
