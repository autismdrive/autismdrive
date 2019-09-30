import {Component, Input, OnInit} from '@angular/core';
import {ApiService} from '../_services/api/api.service';
import {ConfigService} from '../_services/config.service.ts/config';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss']
})
export class FooterComponent {

  constructor(private api: ApiService,
              private config: ConfigService) { }

}
