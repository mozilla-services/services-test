# Pocket E2E tests

End-to-end tests for the [Pocket](https://getpocket.com) button in Firefox.

## How Do I Even?
```sh
$ git clone git@github.com:mozilla-services/services-test.git
$ cd e2e/pocket/
$ npm run pocket
```

The `pocket` npm script will look for the following runtime on your system:
```
--runtime /Applications/Firefox.app/Contents/MacOS/firefox-bin
```

Your mileage may vary.
