import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { NewsItem } from '../_models/news-item';
import { HitType } from '../_models/query';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  heroSlides: NewsItem[] = [
    {
      title: 'Driving discovery',
      description: 'Current studies in autism research',
      url: '/studies',
      type: HitType.STUDY,
      img: '/assets/home/hero-research.jpg',
      imgClass: 'center-center'
    },
    {
      title: 'Offering connections',
      description: 'Enroll in the Autism Registry to get involved in autism research',
      url: '/enroll',
      type: HitType.STUDY,
      img: '/assets/home/hero-enroll.jpg',
      imgClass: 'bottom-center'
    },
    {
      title: 'Engaging the community',
      description: 'Local autism support organizations, online resources, and in-person events',
      url: '/search?Type=location&Type=resource&Type=event',
      type: HitType.STUDY,
      img: '/assets/home/hero-nurse.jpg',
      imgClass: 'center-center'
    },
    {
      title: 'Sharing best practices',
      description: 'Autism training for clinical professionals',
      url: '/search/filter?words=professional%20training',
      type: HitType.STUDY,
      img: '/assets/home/hero-teacher-students.jpg',
      imgClass: 'center-center'
    },
  ];

  newsItems: NewsItem[] = [
    {
      title: 'ABC Event',
      description: 'New ABC Event about XYZ',
      url: '/resource/0',
      type: HitType.EVENT,
      img: '/assets/home/news0.jpg' },
    {
      title: 'XYZ Support Group Location',
      description: 'Charlottesville support group for XYZ',
      url: '/resource/1',
      type: HitType.LOCATION,
      img: '/assets/home/news1.jpg' },
    {
      title: 'ABC XYZ Online Resource',
      description: 'New ABC training available to parents in XYZ',
      url: '/resource/2',
      type: HitType.RESOURCE,
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
