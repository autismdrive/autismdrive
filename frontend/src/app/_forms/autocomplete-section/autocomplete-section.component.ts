import { Component, ViewChild, OnInit, AfterViewInit } from '@angular/core';
import { FieldType } from '@ngx-formly/material';
import { MatInput } from '@angular/material/input';
import { MatAutocompleteTrigger } from '@angular/material/autocomplete';
import { Observable } from 'rxjs';
import { startWith, switchMap, map } from 'rxjs/operators';
import { Organization } from '../../_models/organization';

@Component({
  selector: 'app-autocomplete-section',
  templateUrl: './autocomplete-section.component.html',
  styleUrls: ['./autocomplete-section.component.scss']
})
export class AutocompleteSectionComponent extends FieldType implements OnInit, AfterViewInit {
  @ViewChild(MatInput, { read: MatInput, static: false }) formFieldControl: MatInput;
  @ViewChild(MatAutocompleteTrigger, { read: MatAutocompleteTrigger, static: false }) autocomplete: MatAutocompleteTrigger;

  filter: Observable<Organization[]>;

  ngOnInit() {
    super.ngOnInit();
    this.filter = this.formControl.valueChanges
      .pipe(
        startWith(''),
        map(value => typeof value === 'string' ? value : value.name),
        map(name => this.to.filter(name))
      );
  }

  displayFn(organization?: Organization): string | undefined {
    return organization ? organization.name : undefined;
  }

  ngAfterViewInit() {
    super.ngAfterViewInit();
    // temporary fix for https://github.com/angular/material2/issues/6728
    (<any> this.autocomplete)._formField = this.formField;
  }
}
