# Introduction
This is the API for Autism DRIVE, a platform to support Autism studies and participants.
## Platform
This is a Python3 / Flask based api. It relies on a Relational Database for storing and organizing resources.  It uses Elastic Search as a full text search engine for locating resources.

### Prerequisites
#### Python 3 and python3-dev, and some cryptography libraries
MacOS:
```BASH
brew install python
```

Debian:
```bash
sudo apt-get install python3 python3-dev
sudo apt-get install -y libssl-dev libffi-dev
```

#### PostgreSQL
* MacOS:
[Download and install Postgres.app](https://postgresapp.com). This will install `postgres`, along with the command-line tools, including `psql`, `pg_ctl`, and others. Then update your `PATH` variable to look in the Postgres.app `bin` directory for the relevant Postgres CLI tools.
```BASH
export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"
```

* Debian:
```BASH
apt-get install postgresql postgresql-client
```

#### ElasticSearch
We are currently using version 6, and should look at upgrading this in the future when my hair isn't on fire.
# Debian
https://medium.com/@pierangelo1982/how-to-install-elasticsearch-6-on-ubuntu-64316dc2de1c

#### Angular
```BASH
npm install -g @angular/cli
```

### Project Setup
* Please use Python 3's virtual environment setup, and install the dependencies in requirements.txt
```bash
cd backend
python3 -m venv python-env
source python-env/bin/activate
pip3 install -r requirements.txt
```

## Database Setup
### Create a Database
*NOTE:* The configuration is currently set up to use "ed_pass" as a password.  You will be promoted to enter a password when you connect.
* MacOS:
```BASH
postgres -D /usr/local/var/postgres
createuser --no-createdb --no-superuser --pwprompt ed_user
createdb stardrive -O ed_user ed_platform
createdb stardrive_test -O ed_user ed_platform
```

* Debian
```BASH
sudo su postgres
createuser --no-createdb --no-superuser --pwprompt ed_user
createdb stardrive -O ed_user ed_platform WITH ENCODING = ‘UTF8′
createdb stardrive_test -O ed_user ed_platform
exit
```
If you are using Ubuntu you will likely need to [enable PSQL](https://help.ubuntu.com/community/PostgreSQL#Managing_users_and_rights) to manage its own users.

### Update the Database
You will need to update your database each time you return to do a pull to make sure all the migrations are run. In the `backend` directory, execute the following command:
```BASH
flask db upgrade
```
### Database Reset
If you encounter errors with the database, you can blow it away completely and reset with the following commands in PSQL:
```SQL
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
COMMENT ON SCHEMA public IS 'standard public schema';
```

### Update Data Models
Each time you modify your data models you will need to create new migrations. The following command will compare the database to the code and create new migrations as needed.  You can edit this newly generated file - it will show up under migrations/versions
```BASH
flask db migrate
```

### Load in the seed data
This will pull in initial values into the database.
```BASH
flask initdb
```

## Add a config file
In the `backend` directory, execute the following command:
```BASH
mkdir instance && cp -r config instance/config && cp instance/config/default.py instance/config.py
```

## Run the app
Execute the following at the top level of the repository to start PostgreSQL, flask, and Angular all in one command:
```BASH
./start.sh
```

Or you can run these 3 commands separately:

Database:
```BASH
./start-db.sh
```

Backend:
```BASH
./start-backend.sh
```

Frontend:
```BASH
./start-frontend.sh
```

Alternatively, you could start each of the services individually, using the commands below.

### Start PostgreSQL
```BASH
pg_ctl -D /usr/local/var/postgres start
```

### Start the backend app
In the `backend` directory, execute the following command:
```BASH
flask run
```

### Start the frontend app
In the `frontend` directory, execute the following commands:
```BASH
npm install
ng serve
```

### Stopping the app
Execute the following at the top level of the repository to stop all running services:
```BASH
./stop.sh
```

### Setting up Mailtrap
To test email integration set up an account with [Mailtrap](https://mailtrap.io/)
In your instance config, set your sname and password.
You can find these values in your Mailtrap account in the settings portion of your inbox; you will not find these values in your general account settings as the username and password are specific to each inbox you create.

MAIL_USERNAME = "numbersandletters"
MAIL_PASSWORD = "lettersandnumbers"

Also note that mail is handled differently for tests. Make sure that your instance config has

TESTING = False

## Maintenance

### Clear out the database, indexes, and reseed the database
This will remove all data from the database, delete all information from the ElasticSearch Index, and remove all data and recreate it from the example data files. In the `backend` directory, execute the following command:
```BASH
source python-env/bin/activate
export FLASK_APP=./app/__init__.py
flask cleardb
flask db upgrade
flask initdb
```

### Migration Conflicts
If you find yourself with conflicting migrations, it might be appropriate to resolve with a merge:
```bash
flask db merge -m "merge cc4610a6ece3 and 2679ef53e0bd" cc4610a6ece3 2679ef53e0bd
```
This will auto-generate a new migration that ties the streams together.

### Migrations with Enum columns
Alembic probably will not generate migrations that do everything that you need them to do when it comes to handling Enum values.
Look at migration versions 2fd0ab60fe3a_.py and 5fb917adc751_.py to see some examples of handling enum additions and changes. 
2fd0ab60fe3a_.py shows how to delete an existing column and replace it with an enum (I haven't found a way to simply 
alter the column and get the migrations to upgrade and downgrade successfully). 5fb917adc751_.py shows an example with 
adding a value to the enum list.

## Best Practices
There are a few things I hope to do consistently for this project, to avoid some pitfalls from the [Cadre Academy site](https://education.cadre.virginia.edu/#/home).  When adding code please follow these guidelines:

### Write tests.
Don't commit code that doesn't have at least some basic testing of the new functionality.  Don't commit code without all tests passing.


### Database calls
* Favor db.session.query over using the models for these calls.
```
db.session.query( ...
```
not
```
models.Resrouce.query( ...
```


### Security / Authentication
This will become increasingly complicated, so check back here often.
At present the system can handle single sign on (SSO) authentication through Shibboleth via a
connector on the apache web server that looks for headers we know are provided by the University
of Virginia.  This will change in the future as we migrate to using a OnConnect which will allow
connections with more institutions.  We'll also need to offer direct log-ins for community users.

Once credentials are established, the front end (Angular) and backend (Flask/Python) will use a JWT
token.

#### Develoment Mode
The SSO aspect is bypassed in Development mode.  Clicking the log in button will immediately
log you in as the user specified in your instance/config.py.
```
SSO_DEVELOPMENT_UID = 'dhf8r'
```
I've created users for primary developers in our example_data, and that information is loaded
into the database automatically with a *flask reset*  Add yourself there if needed.

#### Production Mode
In production, the redirect on the front end needs to point to the url that will direct us out to
Shibboleth.  The account we use will send the user back to an API endpoint that will generate a JWT
token, and then redirect again to the front end, passing that token along as a GET parameter.


## Testing

### Run backend tests
Make sure you have set up your test database (see Database Setup above)
You can use nose2 to execute all of tests, or you can run them individually using
Pycharm or other IDE.
In the `backend` directory, execute the following command:
```BASH
source python-env/bin/activate
export FLASK_APP=./app/__init__.py
nose2
```

### Run frontend tests
Make sure you have the database, backend, and frontend all running.

Execute the following at the top level of the repository, which will clear and re-seed the database, then run all e2e tests:
```BASH
./test-e2e.sh
```
Alternatively, to run the e2e tests without reseeding first, execute the following command in the `frontend` directory:
```BASH
ng e2e --dev-server-target=
```

### Public/Private Configuration
For the most part, you don't need to run the second configuration in development unless you are specifically
working on the handoff of data.  The private mirror will pull data from the public instance and then potentially
remove it. 

#### To run the private mirror instance, you'll need a second database:
Run the following command (as postgres) from a bash prompt.
```BASH
createdb stardrive_mirror -O ed_user ed_platform
```

### Configuration
You will need to specify a different configuration file for the private mirror
instance.   A set of reasonable defaults for development is available
under the "mirror.py" in the config directory.  You can set an environment
variable to specify this when you fire up the mirroring instance.

```bash
APP_CONFIG_FILE=/full/path/to/config/mirror.py
```
  
Note that it should be the full path.  You'll be running both instances, 
so don't set this environment variable for all commands, just for running the instance.
For me, I have it set as an environment variable under the Run Configuration within
PyCharm.  I copied by existing run command and added this environment variable
there.  You will also need to add a port (5001) argument so you aren't running on the 
same port as the primary server.  Below are the settings in my Run configuration:

Parameters: 5001
Environment Variable: PYTHONUNBUFFERED=1;MIRRORING=true

You will need to build the basic data structures in the database in order to
load data for this you will need to run the init_db flask command, but
you will need to make that specific to the mirror instance.  You'll need to provide
ALL the environment settings with the flask command for it to work correctly.

```bash
FLASK_APP=app/__init__.py MIRRORING=true flask db upgrade
```

# Production Deployment
You will need to install:
  * Python 3
  * Elastic Search 6
  * Apache Web Server
     * mod-wsgi  (for running flask apps within apache)
  * Postgres 
 
I've tended to set up the website under /var/www/star or /var/www/autismdrive (the new name and url)
In the /var/www/autismdrive/ I create a python virtual enviroment with the command:
```
python3 -m venv python-env
```
When pushing to production please create a new 'Release' on gitHub describing the changes that were rolled out.





 