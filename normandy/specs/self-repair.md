# Self-Repair Test Plan

This document describes the test plan for the self-repair system in Firefox that
SHIELD will be serving.

## Setup

1. [Set up a local instance of Normandy][normandy-docker-qa]. This should
   include running the `python manage.py initial_data` command, which sets up a
   `console-log` action in your local instance. If you don't have this action,
   run the command again.

## Notes

- All URLs pointing to `https://localhost:8000` are meant to refer to your local
  instance of Normandy. You may need to replace the domain in these URLs.
- All tests assume that there are no other enabled recipes in the admin besides
  the ones mentioned in the prep section. It may be useful to disable but not
  delete recipes after testing them to make future testing quicker.

## Test 1: Basic Run Test

### Prep

1. Create a recipe in the admin interface:
   - Name: Basic Self-Repair Test
   - Action: `console-log`
   - Arguments:
     - message: `success`
   - Sample Rate: `1`
   - Enabled: Check
   - Start time: empty
   - End time: empty
   - Locales: empty
   - Countries: empty
   - Release channels: empty

### Test

1. Open `about:config`.
2. Search for a preference named `browser.selfsupport.url` and set it to
   `https://localhost:8000/%LOCALE%/repair`.
3. Close and reopen Firefox.
4. Wait 5 seconds after Firefox opens.
5. Open the Browser Console (available under
   `Tools -> Web Developer -> Browser Console`).
6. Confirm that the `success` message was logged to the console.
