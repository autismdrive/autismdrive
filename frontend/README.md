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

### From PyCharm
Open the Edit Configurations menu (Run > Edit Configurations...) and add a Protractor configuration with the following settings:
* Configuration File: `[path-to-your-files]/star-drive/frontend/e2e/protractor.conf.js`
* Protractor Options: `--dev-server-target=`

Save the configuration. Now you can run end-to-end tests with the play button.

### From command line
Edit the tsconfig file path in the Protractor config file (frontend/e2e/protractor.conf.js):
```
    require('ts-node').register({
      project: './e2e/tsconfig.e2e.json'
    });
```

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

