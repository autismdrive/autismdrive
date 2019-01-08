import { MarkdownService } from 'ngx-markdown';
import { SpyObject, SDSpy } from './helper.mock';

export class MockMarkdownService extends SpyObject {

  compileSpy: SDSpy;
  getSourceSpy: SDSpy;
  highlightSpy: SDSpy;
  fakeResponse: any;

  constructor() {
    super(MarkdownService);
    this.fakeResponse = null;
    this.compileSpy = this.spy('compile').andReturn(this);
    this.getSourceSpy = this.spy('getSource').andReturn(this);
    this.highlightSpy = this.spy('highlight').andReturn(this);
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
