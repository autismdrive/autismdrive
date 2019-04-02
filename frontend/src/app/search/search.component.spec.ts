import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import {
  MatExpansionModule,
  MatFormFieldModule,
  MatIconModule,
  MatInputModule,
  MatListModule,
  MatPaginatorModule,
  MatSidenavModule,
  MatTooltipModule
} from '@angular/material';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ActivatedRoute, Route } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';
import { of as observableOf } from 'rxjs';
import { GradientBorderDirective } from '../gradient-border.directive';
import { Resource } from '../resource';
import { ResourceQuery } from '../resource-query';
import { getDummyResource } from '../shared/fixtures/resource';
import { MockResourceApiService } from '../shared/mocks/resource-api.service.mock';
import { ResourceApiService } from '../shared/resource-api/resource-api.service';
import { SearchComponent } from './search.component';

describe('SearchComponent', () => {
  let api: MockResourceApiService;
  let component: SearchComponent;
  let fixture: ComponentFixture<SearchComponent>;
  const resources: Resource[] = [getDummyResource()];

  beforeEach(async(() => {
    api = new MockResourceApiService();
    const route: Route = { path: 'search', component: SearchComponent, data: { title: 'Search Resources' } };

    TestBed
      .configureTestingModule({
        declarations: [
          SearchComponent,
          GradientBorderDirective
        ],
        imports: [
          BrowserAnimationsModule,
          MatExpansionModule,
          MatFormFieldModule,
          MatIconModule,
          MatInputModule,
          MatListModule,
          MatPaginatorModule,
          MatSidenavModule,
          MatTooltipModule,
          ReactiveFormsModule,
          RouterTestingModule.withRoutes([route])
        ],
        providers: [
          {
            provide: ActivatedRoute,
            useValue: {
              queryParamMap: observableOf({ query: '', keys: [] }),
            }
          },
          { provide: ResourceApiService, useValue: api }
        ],
        schemas: [CUSTOM_ELEMENTS_SCHEMA]
      })
      .compileComponents()
      .then(() => {
        api.spyAndReturnFake('searchResources', resources);
        fixture = TestBed.createComponent(SearchComponent);
        component = fixture.componentInstance;
        component.resourceQuery = new ResourceQuery({
          query: '',
          filters: [],
          facets: [],
          total: 0,
          size: 0,
          start: 0,
          resources: [],
        });
        fixture.detectChanges();
      });
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
