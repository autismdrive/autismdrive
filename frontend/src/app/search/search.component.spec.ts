import {CUSTOM_ELEMENTS_SCHEMA} from '@angular/core';
import {ComponentFixture, TestBed, waitForAsync} from '@angular/core/testing';
import {ReactiveFormsModule} from '@angular/forms';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatIconModule} from '@angular/material/icon';
import {MatInputModule} from '@angular/material/input';
import {MatListModule} from '@angular/material/list';
import {MatPaginatorModule} from '@angular/material/paginator';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatTooltipModule} from '@angular/material/tooltip';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {ActivatedRoute, Route} from '@angular/router';
import {RouterTestingModule} from '@angular/router/testing';
import {of as observableOf} from 'rxjs';
import {SearchComponent} from './search.component';

describe('SearchComponent', () => {
  let component: SearchComponent;
  let fixture: ComponentFixture<SearchComponent>;

  beforeEach(
    waitForAsync(() => {
      const route: Route = {path: 'search', component: SearchComponent, data: {title: 'Search Resources'}};

      TestBed.configureTestingModule({
        declarations: [SearchComponent],
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
          RouterTestingModule.withRoutes([route]),
        ],
        providers: [
          {
            provide: ActivatedRoute,
            useValue: {
              queryParamMap: observableOf({query: '', keys: []}),
            },
          },
        ],
        schemas: [CUSTOM_ELEMENTS_SCHEMA],
      })
        .compileComponents()
        .then(() => {
          fixture = TestBed.createComponent(SearchComponent);
          component = fixture.componentInstance;
          fixture.detectChanges();
        });
    }),
  );

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
