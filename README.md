# Build new version

```sh
poetry version <type>
```

Where `<type>`

- major
- minor
- patch
- premajor
- preminor
- prepatch
- prerelease

https://python-poetry.org/docs/cli/#version

```sh
poetry build
```

https://python-poetry.org/docs/cli/#build

# Test

```sh
poetry run pytest
```

```sh
poetry run coverage run -m pytest && poetry run coverage report -m && poetry run coverage html
```
