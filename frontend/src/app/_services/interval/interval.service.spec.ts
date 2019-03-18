import { TestBed } from '@angular/core/testing';

import { IntervalService } from './interval.service';

describe('IntervalService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: IntervalService = TestBed.get(IntervalService);
    expect(service).toBeTruthy();
  });
});
