# TPS automation

TPS is Testing and Performance for (Firefox) Sync.  It's a test suite that lives in `mozilla-central`.
This piece of automation is designed to run TPS on a designated schedule from an Ubuntu 14.04 LTS node in AWS.

# Steps to follow

#. Create a node (we use a `t2.medium`) using any of the available 14.04 LTS AMIs.
#. Log into the node using `ssh` as the `ubuntu` user.
#. Type: `sudo apt-get -y update && sudo apt-get -y install git make`
#. Type: `mkdir -p Library/github/mozilla-services`
#. Type: `cd Library/github/mozilla-services`
#. Clone this repository in that directory, i.e. `git clone git@github.com:mozilla-services/services-test.git`
#. Type: `cd services-test/sync/e2e-test`
#. Make sure you have the keys necessary to decrypt the `*.asc` files. (How to do this will vary -- ask kthiessen.)
#. Change the `Makefile` so that `CENTRAL` points to a directory with a reasonably recent checkout of `mozilla-central`
#. Type: `sudo make ubuntu`
#. Populate `/home/ubuntu/.mailrc` with a mail-config that will allow sending mail from the `ubuntu` user.
#. Type: `make setup` -- it will print errrors if something bad happens.

That's the one-time node setup.

## Running on a schedule
#. Type: `sudo make cron` (if you want the cronjob to run and send mail.)

## If you want to do a manual test
#. Type `make update` to update the `mozilla-central` tree.
#. Type `make nightly` to download the latest Firefox Nightly.
#. Type `make prod` to run a (very short, should take less than 5 minutes) test against Sync Production.
#. Type `make stage` to run a (longer, will take 20 minutes or so) against Sync Stage.
