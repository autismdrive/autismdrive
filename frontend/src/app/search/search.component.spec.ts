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
import {ActivatedRoute, RouterModule} from '@angular/router';
import {AppModule} from '@app/app.module';
import {MockBuilder, MockedComponentFixture, MockRender} from '@node_modules/ng-mocks';
import {of} from 'rxjs';
import {SearchComponent} from './search.component';

describe('SearchComponent', () => {
  let component: SearchComponent;
  let fixture: MockedComponentFixture<SearchComponent>;

  beforeEach(() => {
    return MockBuilder(SearchComponent, AppModule)
      .keep(BrowserAnimationsModule)
      .keep(MatExpansionModule)
      .keep(MatFormFieldModule)
      .keep(MatIconModule)
      .keep(MatInputModule)
      .keep(MatListModule)
      .keep(MatPaginatorModule)
      .keep(MatSidenavModule)
      .keep(MatTooltipModule)
      .keep(ReactiveFormsModule)
      .keep(RouterModule)
      .provide({
        provide: ActivatedRoute,
        useValue: {
          queryParamMap: of({query: '', keys: []}),
        },
      });
  });

  beforeEach(() => {
    fixture = MockRender(SearchComponent, null, {detectChanges: true});
    component = fixture.point.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
