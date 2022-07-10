Device configs backup utility
====

What's inside?
----

Three command-line utilities:
~~~~
backuper-start for launching backup process

backuper-status for obtaining backup status filtered by date/subnet/model/etc.

backuper-db for managing database state

Help pages:
~~~~
None (at this moment)

HOWTO:
----
backuper-db
~~~~

If postgres url is set via cfg.py or environmental variable:

    backuper-db upgrade head

If postgres url is not set:

    backuper-db --pg-url=postgresql://username:password@host/database upgrade head