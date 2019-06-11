import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { NewsItem } from '../_models/news-item';

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
      type: 'Research Study',
      img: '/assets/home/hero-research.jpg',
      imgClass: 'center-center'
    },
    {
      title: 'Offering connections',
      description: 'Enroll in the Autism Registry to get involved in autism research',
      url: '/enroll',
      type: 'Research Study',
      img: '/assets/home/hero-enroll.jpg',
      imgClass: 'bottom-center'
    },
    {
      title: 'Engaging the community',
      description: 'Local autism support organizations, online resources, and in-person events',
      url: '/search?Type=location&Type=resource&Type=event',
      type: 'Research Study',
      img: '/assets/home/hero-nurse.jpg',
      imgClass: 'center-center'
    },
    {
      title: 'Sharing best practices',
      description: 'Autism training for clinical professionals',
      url: '/search/filter?words=professional%20training',
      type: 'Research Study',
      img: '/assets/home/hero-teacher-students.jpg',
      imgClass: 'center-center'
    },
  ];

  newsItems: NewsItem[] = [
    {
      title: 'ABC Study',
      description: 'New ABC study to explore XYZ in 2020',
      url: '/study/1',
      type: 'Research Study',
      img: '/assets/home/news0.jpg' },
    {
      title: 'XYZ Support Group',
      description: 'Charlottesville support group for XYZ',
      url: '/resource/1',
      type: 'Community Resource',
      img: '/assets/home/news1.jpg' },
    {
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
