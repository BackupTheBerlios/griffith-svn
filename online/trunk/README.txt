This file is for you to describe the WebGriffith application. Typically
you would include information such as the information below:

Installation and Setup
======================


Install ``Pylons`` using your favourite package manader::

    aptitude install python-pylons

Make a config file as follows::

    paster make-config WebGriffith config.ini

Tweak the config file as appropriate and then setup the application::

    paster setup-app development.ini

Then you are ready to go.

Starting application
====================

Development::

    paster serve --reload development.ini

Production::

    paster serve production.ini

