import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { NewsItem } from '../_models/news-item';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  newsItems: NewsItem[] = [
    {
      index: 0,
      title: 'ABC Study',
      description: 'New ABC study to explore XYZ in 2020',
      url: '/study/1',
      type: 'Research Study',
      img: '/assets/home/news0.jpg' },
    {
      index: 1,
      title: 'XYZ Support Group',
      description: 'Charlottesville support group for XYZ',
      url: '/resource/1',
      type: 'Community Resource',
      img: '/assets/home/news1.jpg' },
    {
      index: 2,
      title: 'ABC XYZ Training',
      description: 'New ABC training available to professionals in XYZ',
      url: '/training/1',
      type: 'Training',
      img: '/assets/home/news2.jpg' },
  ];

  constructor(
    private router: Router
  ) { }

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
}
