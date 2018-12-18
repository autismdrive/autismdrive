import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { Resource } from '../resource';

@Component({
  selector: 'app-resources',
  templateUrl: './resources.component.html',
  styleUrls: ['./resources.component.scss']
})
export class ResourcesComponent implements OnInit {
  resources: Resource[];

  constructor(
    private api: ApiService
  ) { }

  ngOnInit() {
    this.loadResources();
  }

  loadResources(){
    this.api.getResources().subscribe(
      (resources) => {
        this.resources = resources;
      }
    )
  }

}
