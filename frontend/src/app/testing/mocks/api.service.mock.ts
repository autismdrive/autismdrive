import { ApiService } from '../../api.service';
import { SpyObject } from './helper.mock';
import Spy = jasmine.Spy;

export class MockApiService extends SpyObject {

  addStudySpy: Spy;
  updateStudySpy: Spy;
  deleteStudySpy: Spy;
  getStudySpy: Spy;
  getStudiesSpy: Spy;
  addResourceSpy: Spy;
  updateResourceSpy: Spy;
  deleteResourceSpy: Spy;
  getResourceSpy: Spy;
  getResourcesSpy: Spy;
  addTrainingSpy: Spy;
  updateTrainingSpy: Spy;
  deleteTrainingSpy: Spy;
  getTrainingSpy: Spy;
  getTrainingsSpy: Spy;
  getFileAttachmentSpy: Spy;
  addFileAttachmentSpy: Spy;
  addFileAttachmentBlobSpy: Spy;
  updateFileAttachmentSpy: Spy;
  getFileAttachmentBlobSpy: Spy;
  deleteFileAttachmentSpy: Spy;
  fakeResponse: any;

  constructor() {
    super(ApiService);
    this.fakeResponse = null;
    this.addStudySpy = this.spy('addStudy').andReturn(this);
    this.updateStudySpy = this.spy('updateStudy').andReturn(this);
    this.deleteStudySpy = this.spy('deleteStudy').andReturn(this);
    this.getStudySpy = this.spy('getStudy').andReturn(this);
    this.getStudiesSpy = this.spy('getStudies').andReturn(this);
    this.addResourceSpy = this.spy('addResource').andReturn(this);
    this.updateResourceSpy = this.spy('updateResource').andReturn(this);
    this.deleteResourceSpy = this.spy('deleteResource').andReturn(this);
    this.getResourceSpy = this.spy('getResource').andReturn(this);
    this.getResourcesSpy = this.spy('getResources').andReturn(this);
    this.addTrainingSpy = this.spy('addTraining').andReturn(this);
    this.updateTrainingSpy = this.spy('updateTraining').andReturn(this);
    this.deleteTrainingSpy = this.spy('deleteTraining').andReturn(this);
    this.getTrainingSpy = this.spy('getTraining').andReturn(this);
    this.getTrainingsSpy = this.spy('getTrainings').andReturn(this);
    this.getFileAttachmentSpy = this.spy('getFileAttachment').andReturn(this);
    this.addFileAttachmentSpy = this.spy('addFileAttachment').andReturn(this);
    this.addFileAttachmentBlobSpy = this.spy('addFileAttachmentBlob').andReturn(this);
    this.updateFileAttachmentSpy = this.spy('updateFileAttachment').andReturn(this);
    this.getFileAttachmentBlobSpy = this.spy('getFileAttachmentBlob').andReturn(this);
    this.deleteFileAttachmentSpy = this.spy('deleteFileAttachment').andReturn(this);
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
