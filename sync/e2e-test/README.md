# TPS automation

TPS is Testing and Performance for (Firefox) Sync.  It's a test suite that lives in `mozilla-central`.
This piece of automation is designed to run TPS on a designated schedule from an Ubuntu 14.04 LTS node in AWS.

# Steps to follow

1. Create a node (we use a `t2.medium`) using any of the available 14.04 LTS AMIs.
1. Log into the node using `ssh` as the `ubuntu` user.
1. Type: `sudo apt-get -y update && sudo apt-get -y install git make`
1. Type: `mkdir -p Library/github/mozilla-services`
1. Type: `cd Library/github/mozilla-services`
1. Clone this repository in that directory, i.e. `git clone git@github.com:mozilla-services/services-test.git`
1. Type: `cd services-test/sync/e2e-test`
1. Make sure you have the keys necessary to decrypt the `*.asc` files. (How to do this will vary -- ask kthiessen.)
1. Change the `Makefile` so that `CENTRAL` points to a directory with a reasonably recent checkout of `mozilla-central`
1. Type: `sudo make ubuntu`
1. Populate `/home/ubuntu/.mailrc` with a mail-config that will allow sending mail from the `ubuntu` user.
1. Type: `make setup` -- it will print errrors if something bad happens.

That's the one-time node setup.

## Running on a schedule
1. Type: `sudo make cron` (if you want the cronjob to run and send mail.)

## If you want to do a manual test
1. Type `make update` to update the `mozilla-central` tree.
1. Type `make nightly` to download the latest Firefox Nightly.
1. Type `make prod` to run a (very short, should take less than 5 minutes) test against Sync Production.
1. Type `make stage` to run a (longer, will take 20 minutes or so) against Sync Stage.
