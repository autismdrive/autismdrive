/// <reference types="cypress" />
import 'cypress-fail-fast';
import 'cypress-network-idle';
require('cypress-terminal-report/src/installLogsCollector')({xhr: {printHeaderData: true}});

declare global {
  namespace Cypress {
    interface Chainable {
      saveLocalStorageCache: () => void;
      restoreLocalStorageCache: () => void;
      clearLocalStorageCache: () => void;
    }
  }
}

let LOCAL_STORAGE_MEMORY = {};
let SESSION_STORAGE_MEMORY = {};

Cypress.Commands.add('saveLocalStorageCache', () => {
  Object.keys(localStorage).forEach(key => {
    LOCAL_STORAGE_MEMORY[key] = localStorage[key];
  });
  Object.keys(sessionStorage).forEach(key => {
    SESSION_STORAGE_MEMORY[key] = sessionStorage[key];
  });
});

Cypress.Commands.add('restoreLocalStorageCache', () => {
  Object.keys(LOCAL_STORAGE_MEMORY).forEach(key => {
    localStorage.setItem(key, LOCAL_STORAGE_MEMORY[key]);
  });
  Object.keys(SESSION_STORAGE_MEMORY).forEach(key => {
    sessionStorage.setItem(key, SESSION_STORAGE_MEMORY[key]);
  });
});

Cypress.Commands.add('clearLocalStorageCache', () => {
  localStorage.clear();
  LOCAL_STORAGE_MEMORY = {};
  sessionStorage.clear();
  SESSION_STORAGE_MEMORY = {};
});
