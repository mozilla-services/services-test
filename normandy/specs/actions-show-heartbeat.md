# `show-heartbeat` Action Test Plan

This document describes the test plan for the `show-heartbeat` action.

- Action code: https://github.com/mozilla/normandy-actions/tree/master/actions/show-heartbeat
- Unit tests: https://github.com/mozilla/normandy-actions/blob/master/test/show-heartbeat.js

## Setup

1. [Set up a local instance of Normandy][normandy-docker-qa].
2. Clone the [normandy-actions][] and follow the steps in the [setup section][]
   of the README to configure the upload script to point to your local instance
   of Normandy.
4. Run the `npm script upload` command to upload the latest versions of actions
   to your local instance.
5. Ensure that in `about:config` you have a setting named
   `browser.uitour.testingOrigins` and that it has the domain and protocol for
   your local Normandy instance in it, such as `https://localhost:8000`.

[normandy-docker-qa]: http://normandy.readthedocs.org/en/latest/qa/docker.html
[normandy-actions]: https://github.com/mozilla/normandy-actions
[setup section]: https://github.com/mozilla/normandy-actions#setup

## Notes

- All URLs pointing to `https://localhost:8000` are meant to refer to your local
  instance of Normandy. You may need to replace the domain in these URLs.
- All tests assume that there are no other enabled recipes in the admin besides
  the ones mentioned in the prep section. It may be useful to disable but not
  delete recipes after testing them to make future testing quicker.

## Test 1: Basic Survey Prompt

### Prep

1. Create a recipe in the admin interface:
   - Name: Basic Survey Prompt
   - Action: `show-heartbeat`
   - Arguments:
     - surveyId: `heartbeat-by-user-first-impression`
     - Default Values:
       - message: `Default message`
       - thanksMessage: `Default thanks`
       - learnMoreMessage: `Default learn more`
       - learnMoreUrl: `http://example.com`
       - postAnswerUrl: `https://example.net`
     - Surveys (create one)
       - title: `default`
       - weight: `1`
   - Sample Rate: `1`
   - Enabled: Check
   - Start time: empty
   - End time: empty
   - Locales: empty
   - Countries: empty
   - Release channels: empty

### Test

1. Navigate to https://localhost:8000/en-US/repair/.
2. Clear localStorage by running `localStorage.clear()` in the web console, and
   open up the Network tab in the DevTools.
3. Reload the page.
4. A Heartbeat prompt should appear with the text `Default message` and a button
   on the right with the text `Default learn more`.
5. The Network tab should show two HTTP POSTs (one on start, one after showing
   the prompt) to `https://input.mozilla.org/api/v2/hb/` with a 200 return
   status.
6. When clicked, the Learn More button should open a new tab to
   `http://example.com`. Another HTTP POST should be sent to Input when the
   button is clicked.
7. After a star rating is clicked, the bar should show the message
   `Default thanks` and open a new tab to `https://example.net`. Another HTTP
   POST to Input should be sent to Input.
8. The post-answer URL (`example.net`) should have URL parameters appended to
   it:
   - `source=heartbeat` should be present.
   - `surveyversion` should be a number.
   - `updateChannel` should be the channel of the Firefox browser being tested,
     e.g. `nightly`.
   - `fxVersion` should be the version of the Firefox browser being tested.
9. Refresh the page. A Heartbeat prompt should no longer appear. In the Storage
   Inspector in the DevTools, localStorage should have at least one entry with
   a key ending in `-lastShown` set to a timestamp value.

## Test 2: Multiple Survey Test

### Prep

1. Create a recipe in the admin interface:
   - Name: Multiple Survey Test
   - Action: `show-heartbeat`
   - Arguments:
     - surveyId: `test-heartbeat`
     - Default Values:
       - message: `Default message`
       - thanksMessage: `Default thanks`
       - learnMoreMessage: `Default learn more`
       - learnMoreUrl: `http://example.com`
       - postAnswerUrl: `https://example.net`
     - Surveys (create two of them)
       - Survey 1
         - title: `Weight 1 Default`
         - weight: `1`
       - Survey 2
         - title: `Weight 3 Custom`
         - message: `Custom message`
         - thanksMessage: `Custom thanks`
         - learnMoreMessage: `Custom learn more`
         - learnMoreUrl: `http://example.com/custom`
         - postAnswerUrl: `https://example.net/custom`
         - weight: `3`
   - Enabled: Check
   - Sample Rate: `1`
   - Start time: empty
   - End time: empty
   - Locales: empty
   - Countries: empty
   - Release channels: empty

### Test

1. Navigate to https://localhost:8000/en-US/repair/?testing (with the testing
   parameter).
2. A Heartbeat prompt should appear. ~25% of the time it will be the "Weight 1
   Default" survey and have the message `Default message`. ~75% of the time it
   will be the "Weight 3 Custom" survey and show the message `Custom message`.
3. Refresh the page a few times and confirm the rough percentages that either
   survey appears are accurate.
4. Confirm that the custom fields on the "Weight 3 Custom" survey take effect as
   described in Test 1.
