import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit{

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
