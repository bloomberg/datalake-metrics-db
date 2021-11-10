# Datalake Metrics DB Migrations

Uses [Alembic](https://alembic.sqlalchemy.org/en/latest/) to create and run migration for a database that stores datalake query metrics.

## Menu

- [Rationale](#rationale)
- [Installation](#installation)
- [Contributions](#contributions)
- [License](#license)
- [Code of Conduct](#code-of-conduct)
- [Security Vulnerability Reporting](#security-vulnerability-reporting)

## Rationale

The purpose of this project is to offer safe migrations for upgrading and downgrading databases that store datalake query metadata and metrics.

## Installation

This is meant to be used with [Trino](https://github.com/trinodb/trino) and models data based on Trino's query metrics. This has been tested with [Trino 363](https://github.com/trinodb/trino/releases/tag/363), backwards or forwards compatibility is not guaranteed.

Before running this you will need to create a new database `datalake_analytics` with a schema called `datalake_metrics`. This is done by hand and is a one-time configuration.

Alembic is set up to read an SQL connection string from the environment variable `SQLALCHEMY_URL`.

You may also set uncomment `sqlalchemy.url` in `alembic.local.ini` and set the connection string there.

Run `alembic -c alembic.local.ini upgrade head` to upgrade the DB to the newest revision.

Run `alembic -c alembic.local.ini downgrade -1` to downgrade the DB one revision.

## Contributions

We :heart: contributions.

Have you had a good experience with this project? Why not share some love and contribute code, or just let us know about any issues you had with it?

We welcome issue reports [here](../../issues); be sure to choose the proper issue template for your issue, so that we can be sure you're providing the necessary information.

Before sending a [Pull Request](../../pulls), please make sure you read our
[Contribution Guidelines](https://github.com/bloomberg/.github/blob/master/CONTRIBUTING.md).

## License

Please read the [LICENSE](LICENSE) file.

## Code of Conduct

This project has adopted a [Code of Conduct](https://github.com/bloomberg/.github/blob/master/CODE_OF_CONDUCT.md).
If you have any concerns about the Code, or behavior which you have experienced in the project, please
contact us at opensource@bloomberg.net.

## Security Vulnerability Reporting

If you believe you have identified a security vulnerability in this project, please send email to the project
team at opensource@bloomberg.net, detailing the suspected issue and any methods you've found to reproduce it.

Please do NOT open an issue in the GitHub repository, as we'd prefer to keep vulnerability reports private until
we've had an opportunity to review and address them.
