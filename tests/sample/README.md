# sample-repo

> **Test fixture** — This directory is a minimal generic repository used by `mokoconsulting/mokostandards` API tests.
> It simulates a real-world repository so that validators such as `check_repo_health.php` and
> `auto_detect_platform.php` can be exercised without network access.

## About

`sample-repo` is a fictional generic PHP project maintained by Moko Consulting.
It exists solely as a testing fixture and should not be treated as production code.

## Installation

```bash
composer install
```

## Usage

```bash
php src/index.php
```

## Development

Run tests:

```bash
./vendor/bin/phpunit
```

Run linters:

```bash
./vendor/bin/phpcs
./vendor/bin/phpstan analyse src/
```

## License

GPL-3.0-or-later — see [LICENSE](./LICENSE).

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).
