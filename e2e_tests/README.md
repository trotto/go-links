For end-to-end tests to run, the config file must have a section like this:

```yaml
testing:
  domains:
    - widgets.trotto.dev
    - gizmos.trotto.dev
  secret: some_secret_for_jwts
```

## Commands

| command | description |
| --- | --- |
| `yarn test` | Runs all tests in headless Chrome. Requires the `TEST_INSTANCE_BASE` environment variable be set |
| `yarn test:dev` | Runs all tests in headless Chrome, using the local dev server |
| `yarn test:dev:single` | Runs a single test in headless Chrome, using the local dev server. Example: `yarn test:dev:single "a user should not be able to access go links from another organization"` |
| `yarn test:debug` | Runs all tests in headful Chrome, using the local dev server |
| `yarn test:debug:single` | Runs a single test in headful Chrome, using the local dev server. Example: `yarn test:debug:single "a user should not be able to access go links from another organization"` |
