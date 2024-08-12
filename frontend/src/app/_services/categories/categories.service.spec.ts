import {TestBed} from '@angular/core/testing';
import {ApiService} from '@services/api/api.service';
import {CategoriesService} from './categories.service';
import {MockProvider} from 'ng-mocks';
import {of} from 'rxjs';

describe('CategoriesService', () => {
  let service: CategoriesService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        CategoriesService,
        MockProvider(ApiService, {
          getCategoryTree: jest.fn().mockReturnValue(of([])),
        }),
      ],
    });
    service = TestBed.inject(CategoriesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
