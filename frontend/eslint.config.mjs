// @ts-check
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import angular from 'angular-eslint';
import pluginCypress from 'eslint-plugin-cypress/flat';
import pluginJest from 'eslint-plugin-jest';
import pluginChaiFriendly from 'eslint-plugin-chai-friendly';

export default tseslint.config(
  {
    files: ['**/*.js'],
    extends: [eslint.configs.recommended],
  },
  {
    files: ['**/*.ts'],
    extends: [
      eslint.configs.recommended,
      ...tseslint.configs.recommended,
      ...tseslint.configs.stylistic,
      ...angular.configs.tsRecommended,
    ],
    processor: angular.processInlineTemplates,
  },
  {
    files: ['./cypress/**/*.ts'],
    extends: [pluginCypress.configs.recommended, pluginChaiFriendly.configs.recommendedFlat],
  },
  {
    files: ['**/*.spec.ts'],
    extends: [pluginJest.configs['flat/recommended'], pluginChaiFriendly.configs.recommendedFlat],
  },
  {
    files: ['**/*.html'],
    extends: [...angular.configs.templateRecommended, ...angular.configs.templateAccessibility],
  },
);
