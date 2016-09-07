# End-to-end test plan for 'x-screen-draw-performance-variations'

## Ownership:

- Author:  Gregg Lind <glind@m.c>
- Test Plan Version: 3

## link to addon

addon: `https://people.mozilla.org/~glind/all/shield-studies-demo-site/x-screen-draw-performance-shield-study-1.xpi`

## General Prep.

Use the shield-variations-gestalt/testing-helper-addon

OR:

1.  Open:

    1. `about:config`
    2. `about:addons`

2.  set:

         1. `general.warnOnAboutConfig`, `false`



## Test 1:  install addon, normal install.

### Prep:

1. `about:config` reset / unset  `nglayout.initialpaint.delay`
2. install addon

### Expect:

1. `about:config`

   check these prefs:

   1.  `extensions.@x-screen-draw-performance-variations-1.firstrun`

           Should be: `1456940036000` or simliar `Date.now()`

   2. `extensions.@x-screen-draw-performance-variations-1.variation`

          Should be:  one of `ut`, `medium`, `aggressive`

### Cleanup

1.  Uninstall addon
2.  Close survey tab.

## Test 2:  install addon, user is ineligible because their pref is already "user set".  Addon should die.

### Prep:

1. In `about:config`

  1. create the pref `nglayout.initialpaint.delay` if it does not exist.  (Right click on the "pref area", `new > interget`)

  2.  set  `nglayout.initialpaint.delay` to `13`

3. install addon

### Expect:

1. addon will briefly install
2. addon will then die (`about:addons` will no longer show it)
3. local prefs (`extensions.@x-screen-draw-performance-variations-1`) are reset
4. NO SURVEY (a new tab with the survey DOES NOT OPEN)
5.     `nglayout.initialpaint.delay` still 13

### Cleanup:

1.  reset `nglayout.initialpaint.delay`

## Test 3: Setup a particular experimental variation choice (branch), then simulate 2nd Startup.

### What:

- During first install, the addon will choose of several variations to implement (for the setting)
- 2nd and subsequent runs should have that same variation.
- here we choose the 'medium' (setting = 50) variation.

### Prep:

1.  reset `nglayout.initialpaint.delay`
2.  create `extensions.@x-screen-draw-performance-variations-1.variation` as 'medium'  (simulates what would happen during first install).

### Expect

1.  open `about:config`
2.  pref `nglayout.initialpaint.delay` will remain `50`


### Cleanup

1.  Uninstall addon
2.  Close survey tab that opens.  (Pref will also reset)


## Test 4: 'end of study'

### Prep:

1.  `about:config`.  Reset `nglayout.initialpaint.delay` if set.
2.  Force a past date.  Create new pref `extensions.@x-screen-draw-performance-variations-1.firstrun` as `500`  (i.e., the dawn of time)
3.  install the addon

### Expect

1.  addon will install successfully
2.  then immediately `die` because it is too old
3.  Observer survey (exactly 1) opened with `reason=end-of-study` in the url.
4.  all `@x-screen` prefs will be cleared

### Cleanup.

1.  Close survey tab.

## Test 5: 'user-disable' the addon. after successful install.

### Prep:

1.  reset `nglayout.initialpaint.delay` if set.
2.  install addon.
3.  from `about:addons` disable or uninstall the addon.


### Expect

1.  tab opens with survey (exactly 1) with `reason=user-ended-study` in the url
2.  all `@x-screen` prefs will be cleared

### Cleanup

1.  Close Survey Tab.


## FAQ

1.  These step are a hassle!

    I know, sorry :(

2.  I have an idea for how to make that better!

    Cool, tell Gregg!

3.  Maybe an addon could do all these steps?

    I agree!  I also run addon tests, but they are way more complicated.  Not quite sure how to automate that part of the build.





