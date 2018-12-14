import { ScrollToService } from '@nicky-lenaers/ngx-scroll-to';
import { SpyObject } from './helper.mock';
import Spy = jasmine.Spy;

export class MockScrollToService extends SpyObject {

  scrollToSpy: Spy;
  fakeResponse: any;

  constructor() {
    super(ScrollToService);
    this.fakeResponse = null;
    this.scrollToSpy = this.spy('scrollTo').andReturn(this);
  }

  subscribe(callback: any) {
    callback(this.fakeResponse);
  }

  setResponse(json: any): void {
    this.fakeResponse = json;
  }

  spyAndReturnFake(methodName: string, fakeResponse: any) {
    this.spy(methodName).andReturn({ subscribe: callback => callback(fakeResponse) });
  }
}
