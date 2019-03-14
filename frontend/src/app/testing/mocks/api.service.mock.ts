import { SpyObject, SDSpy } from './helper.mock';
import { ApiService } from '../../_services/api/api.service';


export class MockApiService extends SpyObject {

  addStudySpy: SDSpy;
  updateStudySpy: SDSpy;
  deleteStudySpy: SDSpy;
  getStudySpy: SDSpy;
  getStudiesSpy: SDSpy;
  addResourceSpy: SDSpy;
  updateResourceSpy: SDSpy;
  deleteResourceSpy: SDSpy;
  getResourceSpy: SDSpy;
  getResourcesSpy: SDSpy;
  addTrainingSpy: SDSpy;
  updateTrainingSpy: SDSpy;
  deleteTrainingSpy: SDSpy;
  getTrainingSpy: SDSpy;
  getTrainingsSpy: SDSpy;
  getFileAttachmentSpy: SDSpy;
  addFileAttachmentSpy: SDSpy;
  addFileAttachmentBlobSpy: SDSpy;
  updateFileAttachmentSpy: SDSpy;
  getFileAttachmentBlobSpy: SDSpy;
  deleteFileAttachmentSpy: SDSpy;
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
