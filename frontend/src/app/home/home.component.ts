import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {Study} from '../_models/study';
import {ApiService} from '../_services/api/api.service';
import {NewsItem} from '../_models/news-item';
import {HitLabel} from '../_models/query';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  currentStudies: Study[];

  constructor(
    private router: Router,
    private api: ApiService
  ) {
    this.api.getStudies().subscribe(all => {
      console.log('all studies:', all);
      this.currentStudies = all.filter(s => s.status === 'currently_enrolling');
    });
  }

  ngOnInit() {
  }

  goEnroll($event) {
    $event.preventDefault();
    this.router.navigate(['enroll']);
  }

  goResources($event) {
    $event.preventDefault();
    this.router.navigate(['resources']);
  }

  studiesToNewsItems(studies: Study[]): NewsItem[] {
    return studies
      .sort((a, b) => (a.id > b.id) ? 1 : -1)
      .map((s, i) => {
        const n: NewsItem = {
          title: s.title,
          description: s.description,
          url: `/study/${s.id}`,
          type: HitLabel.STUDY,
          img: `/assets/home/study${i}.jpg`,
          imgClass: 'center-center',
        };

        return n;
      });
  }
}
