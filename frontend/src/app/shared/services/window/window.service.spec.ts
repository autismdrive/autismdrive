import {PLATFORM_ID} from '@angular/core';
import {TestBed} from '@angular/core/testing';
import {mockWindow} from '@fixtures/mock-window';
import {WindowService} from './window.service';

describe('WindowService', () => {
  let service: WindowService;

  const browserDimensions = {
    width: 1024,
    height: 768,
  };

  const serverDimensions = {
    width: mockWindow.innerWidth,
    height: mockWindow.innerHeight,
  };

  jest.spyOn(globalThis.window, 'innerWidth', 'get').mockReturnValue(browserDimensions.width);
  jest.spyOn(globalThis.window, 'innerHeight', 'get').mockReturnValue(browserDimensions.height);

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [WindowService],
    });
  });

  it('should be created', () => {
    service = TestBed.inject(WindowService);
    expect(service).toBeTruthy();
  });

  it('should return real window on client side', () => {
    // Override the value of PLATFORM_ID token to simulate client-side
    TestBed.overrideProvider(PLATFORM_ID, {useValue: 'browser'});
    service = TestBed.inject(WindowService);

    expect(service.window.innerWidth).toEqual(browserDimensions.width);
    expect(service.window.innerHeight).toEqual(browserDimensions.height);
  });

  it('should return fake window on server side', () => {
    // Override the value of PLATFORM_ID token to simulate server-side
    TestBed.overrideProvider(PLATFORM_ID, {useValue: 'server'});
    service = TestBed.inject(WindowService);
    expect(service.window.innerWidth).toEqual(serverDimensions.width);
    expect(service.window.innerHeight).toEqual(serverDimensions.height);
  });
});
