import { Renderer2 } from '@angular/core';
import { SpyObject } from './helper.mock';
import Spy = jasmine.Spy;

export class MockRenderer2 extends SpyObject {

  addClassSpy: Spy;
  appendChildSpy: Spy;
  createCommentSpy: Spy;
  createElementSpy: Spy;
  createTextSpy: Spy;
  dataSpy: Spy;
  destroySpy: Spy;
  insertBeforeSpy: Spy;
  listenSpy: Spy;
  nextSiblingSpy: Spy;
  parentNodeSpy: Spy;
  removeAttributeSpy: Spy;
  removeChildSpy: Spy;
  removeClassSpy: Spy;
  removeStyleSpy: Spy;
  selectRootElementSpy: Spy;
  setAttributeSpy: Spy;
  setPropertySpy: Spy;
  setStyleSpy: Spy;
  setValueSpy: Spy;
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
