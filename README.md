# ARIA

![Testing](https://github.com/mazzobeg/aria-backend/actions/workflows/test.yml/badge.svg)
![](https://raw.githubusercontent.com/mazzobeg/aria-backend/badges/develop/coverage.svg)

## Install from source
```
flit install
```

## Install from source (dev)
To install the project, execute the following command.
```bash
flit install --symlink
```
This way the project will be modified on the fly during development.

To launch aria-backend run the following command.
```bash
aria-backend -c <config_path>
```

Here is an example of minimum configuration.
```json
{
    "SQLALCHEMY_DATABASE_URI": "sqlite:///<path_to_database>.db"
}
```

```zsh
cd src && flask -A aria_backend run && cd ..
```