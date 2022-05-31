=============
Study Buffalo
=============

|Coverage|_ |License|_

.. |Coverage| image:: https://codecov.io/gh/studybuffalo/studybuffalo/branch/master/graph/badge.svg
   :alt: Codecov code coverage

.. _Coverage: https://codecov.io/gh/studybuffalo/studybuffalo

.. |License| image:: https://img.shields.io/github/license/studybuffalo/studybuffalo.svg
   :alt: License

.. _License: https://github.com/studybuffalo/studybuffalo/blob/master/LICENSE

The website and applications of the Study Buffalo.

------------------
What You Will Find
------------------

Hello, we are the Study Buffalo! We are excited to see you taking an interest
in our project. This area is specifically the web hosting side of our
projects. This website is currently created with the Django framework.

---------
Licensing
---------

We strive to keep our projects accessible to all. Everything here is open
source under the GNU Public License version 3. We are always open to
discussing other licensing options, so please contact us if this is an
issue for you.

----------
Contact Us
----------
You can always get a hold of us at studybuffalo@gmail.com,
info@studybuffalo.com, or through GitHub itself.

----------------------------------
Setting Up Development Environment
----------------------------------

1. Install `Python 3.8`_::

.. _Python 3.8: https://www.python.org/downloads/release/python-3812/

2. Install PostgreSQL_ (version 9.4 or higher is required). You will need to
   create an admin account to create the required databases. You may use
   whatever interface you wish to run SQL commands; the following instructions
   assume you are using a commandline interace tool, such as psql.

.. _PostgreSQL: https://www.postgresql.org/download/

3. Once PostgreSQL is installed you will need to create a database and user for
   Django. The following provides a minimal setup with some sane defaults (you
   may update the ``database_name``, ``user``, and ``password`` sections to
   whatever you prefer)::

    CREATE DATABASE database_name;
    CREATE USER user WITH PASSWORD 'password';
    ALTER ROLE user SET client_encoding TO 'utf8';
    ALTER ROLE user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE user SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE database_name TO user;
    ALTER USER user CREATEDB;
    ALTER DATABASE database_name OWNER TO user;

4. Install ``pipenv`` via command line::

    $ pip install pipenv

5. Clone the github repository
   (https://github.com/studybuffalo/studybuffalo.git)

6. In the ``/config/settings`` directory of the repo copy the
   ``.study_buffalo.env`` file and rename it ``study_buffalo.env``

7. If needed, update the variables in the ``study_buffalo.env`` file to use
   your database credentials and any secret keys/API details.

8. In the root directory of the repository, run the Makefile install
   command to setup Django.

   You may setup the environment with no database content with the
   following command::

    $ make --file=Makefile install-development-fresh

   You may setup the environment with fixture content with the
   following command::

    $ make --file=Makefile install-development-fixtures

9. You should now be able to run the Django development server. You can test
   this with the following command, which will generate output similar to
   below::

    $ pipenv run python manage.py runserver 127.0.0.1:8000

    > Performing system checks...
    > System check identified no issues (0 silenced).
    > Django version #.#.#, using settings 'config.settings.development'
    > Starting development server at http://127.0.0.1:8000/
    > Quit the server with CTRL-BREAK.

10. If fixture data was loaded, the following user accounts will be
    available:

    - **Admin Account**: ``username`` = ``admin``, ``email`` =
      ``admin@email.com``, and ``password`` = ``admin``
    - **Basic User Account**: ``username`` = ``user``, ``email`` =
      ``user@email.com``, and ``password`` = ``user``

    **DO NOT** use these accounts in a production environment.


--------------------------
Running development server
--------------------------

To start the development server::

  $ pipenv run python manage.py runserver 127.0.0.1:8000


-------------
Running Tests
-------------

To run tests::

  $ pipenv run pytest

To generate coverage report::

  # XML Report
  $ pipenv run pytest --cov study_buffalo --cov-report xml

  # HTML Report
  $ pipenv run pytest --cov study_buffalo --cov-report html

---------------
Running Linters
---------------

To run linting::

  # Run Pylint
  $ pipenv run pylint study_buffalo/ config/

  # Run Pycodestyle
  $ pipenv run pycodestyle study_buffalo/ config/

-------------------
Documentation Style
-------------------

Docstrings are documented using the reStructuredText format. Details of
this style can be found here:
https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html
