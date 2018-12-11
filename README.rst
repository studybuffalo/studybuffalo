Study Buffalo
=============

|BuildStatus|_ |Coverage|_ |License|_

.. |BuildStatus| image:: https://travis-ci.org/studybuffalo/studybuffalo.svg?branch=master
   :alt: Travis-CI build status

.. _BuildStatus: https://travis-ci.org/studybuffalo/studybuffalo

.. |Coverage| image:: https://codecov.io/gh/studybuffalo/studybuffalo/branch/master/graph/badge.svg
   :alt: Codecov code coverage

.. _Coverage: https://codecov.io/gh/studybuffalo/studybuffalo

.. |License| image:: https://img.shields.io/github/license/studybuffalo/studybuffalo.svg
   :alt: License

.. _License: https://github.com/studybuffalo/studybuffalo/blob/master/LICENSE

The website and applications of the Study Buffalo.

What You Will Find
------------------
Hello, we are the Study Buffalo! We are excited to see you taking an interest
in our project. This area is specifically the web hosting side of our
projects. This website is currently created with the Django framework.

Licensing
---------
We strive to keep our projects accessible to all. Everything here is open
source under the GNU Public License version 3. We are always open to
discussing other licensing options, so please contact us if this is an
issue for you.

Contact Us
----------
You can always get a hold of us at studybuffalo@gmail.com,
info@studybuffalo.com, or through GitHub itself.


Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this the standard Django command:

.. code:: shell

    $ python manage.py createsuperuser


Test coverage
^^^^^^^^^^^^^

To run the tests:

.. code:: shell

    $ pipenv run coverage run manage.py test

To generate a coverage report (HTML):

.. code:: shell

    $ pipenv run coverage html

