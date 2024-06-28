const {pathsToModuleNameMapper} = require('ts-jest');
const {compilerOptions} = require('./tsconfig');
const esModules = ['@angular', '@testing-library', 'ngx-markdown'];

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

module.exports = {
  preset: 'jest-preset-angular',
  roots: ['<rootDir>/src/'],
  testMatch: ['**/+(*.)+(spec).+(ts)'],
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
  collectCoverage: true,
  coverageReporters: ['lcov', 'html'],
  coverageDirectory: 'coverage',
  maxWorkers: 8,
  moduleNameMapper: pathsToModuleNameMapper(compilerOptions.paths || {}, {
    prefix: '<rootDir>/',
  }),
  transform: {
    '.js': 'jest-esm-transformer-2',
  },
  transformIgnorePatterns: [`node_modules/(?!(${esModules.join('|')})/)`],
  globals: {
    addeventatc: {refresh: () => {}},
  },
};
