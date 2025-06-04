import {createRequire} from 'module';
import {pathsToModuleNameMapper} from 'ts-jest';

const tsconfigJSON = createRequire(import.meta.url)('./tsconfig.json');

const esModules = [
  '@angular',
  '@ng-maps',
  '@ngbracket',
  '@ngx-formly',
  '@testing-library',
  '@types/google.maps',
  '@yellowspot/ng-truncate',
  'data-uri-to-buffer',
  'fetch-blob',
  'formdata-polyfill',
  'jsdom-worker',
  'lodash-es',
  'ng2-pdfjs-viewer',
  'ngx-device-detector',
  'ngx-markdown',
  'ngx-progressbar',
  'node-fetch',
];

class StorageMock {
  constructor() {
    this.store = {};
  }

  clear() {
    this.store = {};
  }

  getItem(key) {
    return this.store[key] || null;
  }

  setItem(key, value) {
    this.store[key] = String(value);
  }

  removeItem(key) {
    delete this.store[key];
  }

  get length() {
    return Object.keys(this.store).length;
  }

  key(index) {
    return Object.keys(this.store)[index];
  }
}

global.localStorage = new StorageMock();
global.sessionStorage = new StorageMock();

export default {
  preset: 'jest-preset-angular',
  roots: ['<rootDir>/src/'],
  testMatch: ['**/+(*.)+(spec).+(ts)'],
  setupFiles: ['jsdom-worker'],
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
  collectCoverage: true,
  coverageReporters: ['lcov', 'html'],
  coverageDirectory: 'coverage',
  maxWorkers: 1,
  moduleNameMapper: pathsToModuleNameMapper(tsconfigJSON.compilerOptions.paths || {}, {
    prefix: '<rootDir>/',
  }),
  testEnvironment: '@happy-dom/jest-environment',
  transform: {
    '.js': 'jest-esm-transformer-2',
  },

  transformIgnorePatterns: [`node_modules/(?!(${esModules.join('|')})/)`],
  globals: {
    addeventatc: {
      refresh: () => {},
    },
    YT: {
      PlayerVars: {},
      ClosedCaptionsLoadPolicy: {ForceOn: 1},
      ModestBranding: {Modest: 1},
      RelatedVideos: {Hide: 0},
      ShowInfo: {Hide: 0},
    },
  },
};
