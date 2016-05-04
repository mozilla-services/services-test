# Recipe Filter Test Plan

This document describes the test plan for recipe filtering in Normandy.

## Setup

1. [Set up a local instance of Normandy][normandy-docker-qa]. This should
   include running the `python manage.py initial_data` command, which sets up a
   `console-log` action in your local instance. If you don't have this action,
   run the command again.

[normandy-docker-qa]: http://normandy.readthedocs.org/en/latest/qa/docker.html

## Notes

- All URLs pointing to `https://localhost:8000` are meant to refer to your local
  instance of Normandy. You may need to replace the domain in these URLs.
- All tests assume that there are no other enabled recipes in the admin besides
  the ones mentioned in the prep section. It may be useful to disable but not
  delete recipes after testing them to make future testing quicker.

## Test 1: Start and End Times

### Prep

1. Create a recipe in the admin interface:
   - Name: Start/End Time Tests
   - Action: `console-log`
   - Arguments:
     - message: `success`
   - Enabled: Check
   - Sample Rate: `1`
   - Start time: Sometime soon
   - End time: A minute or so after the start time
   - Locales: empty
   - Countries: empty
   - Release channels: empty

### Test

1. Navigate to https://localhost:8000/en-US/repair/?testing.
2. Confirm that, when refreshing the page, the `success` message is only logged
   to the console if the current time is between the start and end times. Note
   that times in the admin interface are specified in UTC.


## Test 2: Locale Filtering

### Prep

1. Create a recipe in the admin interface:
   - Name: Locale Filtering Tests
   - Action: `console-log`
   - Arguments:
     - message: `success`
   - Enabled: Check
   - Sample Rate: `1`
   - Start time: empty
   - End time: empty
   - Locales: en-US and fr
   - Countries: empty
   - Release channels: empty

### Test

1. Navigate to https://localhost:8000/en-US/repair/?testing.
2. Confirm that the `success` message is logged to the web console.
3. Navigate to https://localhost:8000/fr/repair/?testing.
4. Confirm that the `success` message is logged to the web console.
5. Navigate to https://localhost:8000/pt-BR/repair/?testing.
6. Confirm that the `success` message is __not__ logged to the web console.


## Test 3: Release Channel Filtering

### Prep

1. Create a recipe in the admin interface:
   - Name: Release Channel Filtering Tests
   - Action: `console-log`
   - Arguments:
     - message: `success`
   - Enabled: Check
   - Sample Rate: `1`
   - Start time: empty
   - End time: empty
   - Locales: empty
   - Countries: empty
   - Release channels: aurora

### Test

1. Navigate to https://localhost:8000/en-US/repair/?testing using a release
   build of Firefox.
2. Confirm that the `success` message is __not__ logged to the web console.
3. Navigate to https://localhost:8000/en-US/repair/?testing using a Dev Edition
   build of Firefox.
4. Confirm that the `success` message is logged to the web console.
