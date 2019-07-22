import { Component, OnInit } from '@angular/core';
import { FieldType } from '@ngx-formly/material';
import { Observable } from 'rxjs';
import { startWith, map } from 'rxjs/operators';
import { Organization } from '../../_models/organization';

@Component({
  selector: 'app-autocomplete-section',
  templateUrl: './autocomplete-section.component.html',
  styleUrls: ['./autocomplete-section.component.scss']
})
export class AutocompleteSectionComponent extends FieldType implements OnInit {

  filteredOptions: Observable<Organization[]>;

  ngOnInit() {
    this.filteredOptions = this.formControl.valueChanges
      .pipe(
        startWith(''),
        map(value => typeof value === 'string' ? value : value.name),
        map(name => this.to.filter(name))
      );
  }

  displayFn(organization?: Organization): string | undefined {
    return organization ? organization.name : undefined;
  }
}
