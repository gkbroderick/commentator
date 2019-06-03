# commentator
Django app using [KEXP](https://kexp.org/)'s [playlist feed](http://128.208.196.80/) to add playlist comments to a PSQL backend.

---
##Local Setup Quickstart Version
This assumes Python3.6 and Postgres are installed.

###OS vars
Set up a virtual environment with these OS variables (though secret key is somewhat arbitrary):
```
DB_NAME=database_name
DB_USER=database_user
DB_PASSWORD=database_password
DJANGO_SECRET_KEY='fp3xwka$0_vlq=9velgupm3@bl0kujs3**5a!=2wm-8n^)qy1j'
```
(alternatively, if not using a virtual environment, update them in `commentator/settings.py`, though this is not recommended)

###Database setup
In psql, create `database_user` with `database_password`, then `database_name` with owner  `database_user`. Make sure the `database_user` can create databases for running tests.

###Python dependencies

Hopefully inside your virtual environment, install Python dependencies:
```
pip3 install -r requirements.txt
```
The Django commentator app should now be ready to run locally after migrations.

###Frontend Processing (optional)
Included in the repo is the processed stylesheets and vendor js inside the `frontend` app. If you need to re-run the frontend Gulp system, with Node installed, run `npm install` and run a pre-processor pass with `gulp out`.

---
##Project Requirements
  - Create a Django project
  - Create a URLs path that maps to “Playlist”
  - Create at least one Django App
  - Create at least one model and migration
  - Use https://legacy-api.kexp.org/ API to pull your play data
  - Display all current plays for the last 60 minutes
  - Add ability to make a comment on each play row
  - Add ability to save play row comment to a backend Postgres database
  - Add ability to update play row comment
  - Write at least two test cases around your model behavior

---
##Project Assumptions
  - Only going to be used on the American west coast (simplifying UTC conversion)
  - no user account system necessary (all comments are anonymous)
  - only “media play” and “airbreak” items are necessary to list
  - using a virtual environment for local setup
  - the “playid” of each play instance from the KEXP Legacy API is unique

---
##Local Setup Verbose Version

Make sure you have Python (preferably Python3.6 with Pip), Postgres, and Node (though please note Node is only required if you need to alter the frontend) installed on your machine. All three should be available with [Homebrew](https://brew.sh/).

###Virtual Environment Setup and OS variables
Set up a virtual environment for handling OS variables and installing the project's Python packages non-globally. There are a few ways to setup a virtual environment for Python. I use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/#) locally.

Using venvwrapper, create a virtual environment with:
```
mkvirtualenv -p python3 project_name
```
To get out of the virtual environment, simply type `deactivate`. To activate and work within it again, `workon project_name`.

Set a directory for the Virtual Environment to automatically go to on activation by working on the virtual environment, and in the case of the current working directory, enter in:
```
setvirtualenvproject $VIRTUAL_ENV .
```

####Setting the necessary OS variables for the virtual environment

Inside your virtual environment, it's necessary to set up several variables to ensure Django has access to the Postgres database credentials and the crypto key without exposing them. You can set them once inside your virtual environment by editing its `postactivate` and `predeactivate` scripts.

You'll want to come up with a database name, user, and password for that user before this step, if you haven't already set up a PSQL database.

Edit `$VIRTUAL_ENV/bin/postactivate` to include:
```
export DB_NAME=database_name
export DB_USER=database_user
export DB_PASSWORD=database_password
export DJANGO_SECRET_KEY='fp3xwka$0_vlq=9velgupm3@bl0kujs3**5a!=2wm-8n^)qy1j'

```
Please note this is using a sample SECRET_KEY suitable only for development use. If moving into production replace this with a new secret key

Also edit  `$VIRTUAL_ENV/bin/predeactivate` to include:

```
unset DB_NAME
unset DB_USER
unset DB_PASSWORD
unset DJANGO_SECRET_KEY

```

###Postgres Setup

Enter the Postgres CLI with
```
psql
```
Then, using the same database name, user, and password titles entered into the postactivate script above, create the user:

```
CREATE USER database_user WITH PASSWORD 'database_password';
```

And the database:
```
CREATE DATABASE database_name WITH OWNER database_user;
```

Also, give the database user permission to create test databases in order to run tests:
```
ALTER USER database_user CREATEDB;
```
See Django setup for information on then migrating model information to the DB.

###Python Dependency Setup
Inside your virtual environment, install Python dependencies:
```
pip3 install -r requirements.txt
```

If new dependencies are added, save with:
```
pip3 freeze > requirements.txt

```
Note these could simply be `pip` instead of `pip3` depending on your machine's Python setup.


###Gulp Frontend

This project uses the gulp pre-processor system to process Sass to CSS and minify/Concat JS for production. A production version of the current stylesheet should be saved to the main repo so this is optional in the event the frontend app needs alteration.

####Installation
Install Node dependencies by going to the project directory and entering:
```
npm install
```
This should install all Node packages outlined in `package.json`. You may need to change your Node version to `8.11.3` via [NVM (node Version Manager)](https://github.com/creationix/nvm).

####Gulp Usage

The default action, `gulp`, will process files from `frontend/gulp-src` into a debuggable dev version into its output directory, in this case `frontend/static/frontend/` and start a watch on the src directory. Stop this watch at any time with ctrl + c.

`gulp --out production` will output a production-ready file from `./gulp-src` to `./production`. This should minify code without sourcemaps and so is not recommended for debugging.

---

##Resources Used

###django 1.11 docs (fairly extensively):
  - https://docs.djangoproject.com/en/1.11/

###datetime editing:
  - https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
  - https://stackoverflow.com/questions/17594298/date-time-formats-in-python
  - https://stackoverflow.com/questions/969285/how-do-i-translate-an-iso-8601-datetime-string-into-a-python-datetime-object
  - https://stackoverflow.com/questions/27442756/python-django-templates-timezone-issue
  - https://stackoverflow.com/questions/7065164/how-to-make-an-unaware-datetime-timezone-aware-in-python
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toLocaleString

###form handling:
  - https://stackoverflow.com/questions/46310867/stop-page-from-redirecting-after-form-submission-in-django
  - https://stackoverflow.com/questions/2476382/how-to-check-if-a-textarea-is-empty-in-javascript-or-jquery

###Ajax:
  - https://docs.djangoproject.com/en/1.11/ref/csrf/
  - http://api.jquery.com/jquery.ajax/
  - https://simpleisbetterthancomplex.com/tutorial/2016/08/29/how-to-work-with-ajax-request-with-django.html

###templates:
  - https://stackoverflow.com/questions/11481499/django-iterate-number-in-for-loop-of-a-template

###styling:
  - https://getbootstrap.com/docs/4.0/layout/grid/
  - https://getbootstrap.com/docs/4.0/utilities/spacing/
  - https://developer.mozilla.org/en-US/docs/Web/CSS/white-space

###testing:
  - https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
  - https://docs.djangoproject.com/en/1.11/topics/testing/
  - https://stackoverflow.com/questions/31236237/django-how-to-test-a-not-null-field
  - https://stackoverflow.com/questions/16214846/test-if-validationerror-was-raised
  - https://www.ericholscher.com/blog/2009/apr/16/testing-ajax-views-django/
  - https://stackoverflow.com/questions/40995424/django-and-json-ajax-testing
