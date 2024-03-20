import {ActivatedRoute} from '@angular/router';
import {SDSpy, SpyObject} from './helper.mock';

export class MockActivatedRoute extends SpyObject {
  urlSpy: SDSpy;
  paramsSpy: SDSpy;
  queryParamsSpy: SDSpy;
  fragmentSpy: SDSpy;
  dataSpy: SDSpy;
  fakeResponse: any;

  constructor() {
    super(ActivatedRoute);
    this.fakeResponse = null;
    this.urlSpy = this.spy('url').andReturn(this);
    this.paramsSpy = this.spy('params').andReturn(this);
    this.queryParamsSpy = this.spy('queryParams').andReturn(this);
    this.fragmentSpy = this.spy('fragment').andReturn(this);
    this.dataSpy = this.spy('data').andReturn(this);
  }

  subscribe(callback: any) {
    callback(this.fakeResponse);
  }

  setResponse(json: any): void {
    this.fakeResponse = json;
  }

  spyAndReturnFake(methodName: string, fakeResponse: any) {
    this.spy(methodName).andReturn({subscribe: callback => callback(fakeResponse)});
  }
}
