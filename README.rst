.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

============
imio.monitor
============

Package used to monitor our instances based on plone.restapi.
We add "@monitor" component


Probes
------

Currently supported probes:

- cache_size -- cache sizes informations
- check_smtp -- Check if SMTP is initialize, return number of errors found.
- check_upgrade_steps -- Check if all upgrade steps are ran.
- conflictcount -- number of all conflict errors since startup
- count_users -- the total amount of users in your plone site
- count_valid_users -- Count all users connected since 90 days
- cpu_times --
- creation_date_plonesite -- Get creation date of plonesite object. Default return unix_time (defaut=True) if you want ISO time call 'False' attr.
- dbactivity -- number of load, store and connections on database (default=main) for the last x minutes (default=5)
- dbinfo -- Get database statistics
- dbsize -- size of the database (default=main) in bytes
- errorcount -- number of error present in error_log (default in the root).
- help -- Get help about server commands
- interactive -- Turn on monitor's interactive mode
- last_login_time -- Get last login time user. Default return unix_time
- last_modified_plone_object_time -- Get last modified plone object time. Default return unix_time (defaut=True) if you want ISO time call 'False' attr.
- last_modified_zope_object_time -- Get last modified zope object time. Default return unix_time (defaut=True) if you want ISO time call 'False' attr.
- memory_percent --
- objectcount -- number of object in the database (default=main)
- refcount -- the total amount of object reference counts
- requestqueue_size -- number of requests waiting in the queue to be handled by zope threads
- threads -- Dump current threads execution stack
- unresolved_conflictcount -- number of all unresolved conflict errors since startup
- uptime -- uptime of the zope instance in seconds
- zeocache -- Get ZEO client cache statistics
- zeostatus -- Get ZEO client status information


Examples
--------

This add-on can be seen in action at the following sites:
- Is there a page on the internet where everybody can see the features?


Documentation
-------------

Full documentation for end users can be found in the "docs" folder, and is also available online at http://docs.plone.org/foo/bar


Installation
------------

Install imio.monitor by adding it to your buildout::

    [buildout]

    ...

    eggs =
        imio.monitor


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/imio/imio.monitor/issues
- Source Code: https://github.com/imio/imio.monitor


License
-------

The project is licensed under the GPLv2.
