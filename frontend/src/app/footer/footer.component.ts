import {Component, Input, OnInit} from '@angular/core';
import {ApiService} from '../_services/api/api.service';
import {Status} from '../_models/status';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss']
})
export class FooterComponent {

  @Input() status: Status;

  constructor(private api: ApiService) { }

}
