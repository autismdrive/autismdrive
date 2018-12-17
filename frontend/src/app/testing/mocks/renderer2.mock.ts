import { Renderer2 } from '@angular/core';
import { SpyObject, SDSpy } from './helper.mock';

export class MockRenderer2 extends SpyObject {

  addClassSpy: SDSpy;
  appendChildSpy: SDSpy;
  createCommentSpy: SDSpy;
  createElementSpy: SDSpy;
  createTextSpy: SDSpy;
  dataSpy: SDSpy;
  destroySpy: SDSpy;
  insertBeforeSpy: SDSpy;
  listenSpy: SDSpy;
  nextSiblingSpy: SDSpy;
  parentNodeSpy: SDSpy;
  removeAttributeSpy: SDSpy;
  removeChildSpy: SDSpy;
  removeClassSpy: SDSpy;
  removeStyleSpy: SDSpy;
  selectRootElementSpy: SDSpy;
  setAttributeSpy: SDSpy;
  setPropertySpy: SDSpy;
  setStyleSpy: SDSpy;
  setValueSpy: SDSpy;
  data: any;

  constructor() {
    super(Renderer2);
    this.data = null;
    this.addClassSpy = this.spy('addClass').andReturn(this);
    this.appendChildSpy = this.spy('appendChild').andReturn(this);
    this.createCommentSpy = this.spy('createComment').andReturn(this);
    this.createElementSpy = this.spy('createElement').andReturn(this);
    this.createTextSpy = this.spy('createText').andReturn(this);
    this.dataSpy = this.spy('data').andReturn(this);
    this.destroySpy = this.spy('destroy').andReturn(this);
    this.insertBeforeSpy = this.spy('insertBefore').andReturn(this);
    this.listenSpy = this.spy('listen').andReturn(this);
    this.nextSiblingSpy = this.spy('nextSibling').andReturn(this);
    this.parentNodeSpy = this.spy('parentNode').andReturn(this);
    this.removeAttributeSpy = this.spy('removeAttribute').andReturn(this);
    this.removeChildSpy = this.spy('removeChild').andReturn(this);
    this.removeClassSpy = this.spy('removeClass').andReturn(this);
    this.removeStyleSpy = this.spy('removeStyle').andReturn(this);
    this.selectRootElementSpy = this.spy('selectRootElement').andReturn(this);
    this.setAttributeSpy = this.spy('setAttribute').andReturn(this);
    this.setPropertySpy = this.spy('setProperty').andReturn(this);
    this.setStyleSpy = this.spy('setStyle').andReturn(this);
    this.setValueSpy = this.spy('setValue').andReturn(this);
  }

  subscribe(callback: any) {
    callback(this.data);
  }

  setResponse(json: any): void {
    this.data = json;
  }

  spyAndReturnFake(methodName: string, fakeResponse: any) {
    this.spy(methodName).andReturn({ subscribe: callback => callback(fakeResponse) });
  }
}
