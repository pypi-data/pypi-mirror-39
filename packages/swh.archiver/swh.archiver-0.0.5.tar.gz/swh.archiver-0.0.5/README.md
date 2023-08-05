swh-archiver
============

Orchestrator in charge of guaranteeing that object storage content is pristine
and available in a sufficient amount of copies.

Tests
-----

This module's tests need a postgres db to run. It is recommended to run 
those but they can be skipped:

- `make test`:      will run all tests
- `make test-nodb`: will run only tests that do not need a local DB
- `make test-db`:   will run only tests that do need a local DB

If you do want to run DB-related tests, you should ensure you have access with
sufficient privileges to a Postgresql database.

### Using your system database

You need to:

- ensure that your user is authorized to create and drop DBs, and in particular
  DBs named "softwareheritage-test" and "softwareheritage-dev"

- ensure that you have the storage testdata repository checked out in
  ../swh-storage-testdata

### Using pifpaf

[pifpaf](https://github.com/jd/pifpaf) is a suite of fixtures and a
command-line tool that allows to start and stop daemons for a quick throw-away
usage.

It can be used to run tests that need a Postgres database without any other
configuration reauired nor the need to have special access to a running
database:

```bash

$ pifpaf run postgresql make test-db
[snip]
----------------------------------------------------------------------
Ran 12 tests in 0.903s

OK
```

Note that pifpaf is not yet available as a Debian package, so you may have to
install it in a venv.
