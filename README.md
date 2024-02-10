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
    "SQLALCHEMY_DATABASE_URI": "sqlite:///<path_to_database>.db
}
```