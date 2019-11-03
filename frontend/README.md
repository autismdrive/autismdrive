# Autism DRIVE

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 7.0.5.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

In some circumstances you may want to run the server in "mirror" mode to debug the system running in this configuration.  You can do this with
```
ng serve -c mirror --port 4201 --optimization=false
```
IMPORTANT:  This is purely for deployment/configuration settings.  The system will actually change behavior based on the responses from the backend system,
and should not look at this setting to determine if it is providing a UI for the private mirror vs the public interface.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

## Running unit tests
If we had unit tests, you would run
Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).
But we just have e2e tests on the front end at this time.

## Running end-to-end tests
Make sure you have the database, backend, and frontend all running.

Execute the following at the top level of the repository, which will clear and re-seed the database, then run all e2e tests:
```BASH
./test-e2e.sh
```
Alternatively, to run the e2e tests without reseeding first, execute the following command in the `frontend` directory:
```BASH
ng e2e --dev-server-target=
```

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).


## API keys

Place any API keys in a file called `api-keys.ts` in the `frontend/src` directory. Note that it will be ignored by the `.gitignore` file and will not be committed to the repository. The file must be in the following format:

```ts
const keys = {
  gcp: {
    dev: 'PASTE_DEV_API_KEY_HERE',
    staging: 'PASTE_STAGING_API_KEY_HERE',
    production: 'PASTE_PRODUCTION_API_KEY_HERE'
  }
};

export default keys;
```

In the app, When you need an API key, just import the `keys` object from `api-keys.ts`. For instance, in `frontend/src/environments/environment.prod.ts`:

```ts
import keys from '../api-keys';

export const environment = {
  production: true ,
  api: 'http://http://34.224.58.224/api',
  gcp_api_key: keys.gcp.production
};
```

 