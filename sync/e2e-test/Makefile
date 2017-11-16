
## before you do anything else:
## $ sudo apt-get -y update
## $ sudo apt-get -y install git make

# directory containing a recent hg checkout of mozilla-central
# might automate this later -- but that first checkout
# is dreadfully slow.

CENTRAL=/mnt/extra/mozilla-central

.PHONY: ubuntu cron setup update nightly stage prod

# root-required setup
# might call this "install" instead -- it needs root permissions
# so, "sudo make ubuntu"
ubuntu:
	apt-get -y update
	env PAGER=cat apt-get -y --purge dist-upgrade
	apt-get -y --purge autoremove
	apt-get -y clean
	apt-get -y install mercurial heirloom-mailx

# this also needs root
# so, "sudo make cron"
cron:
	cp -i cron.hourly/* /etc/cron.hourly/
	cp -i cron.daily/*  /etc/cron.daily/

# The part of setup that doesn't need root
# The gpg lines below will probably get replaced with sops eventually
setup:
	ln -sf ${CENTRAL} mozilla-central
	fgrep -q kthiessen /home/ubuntu/.mailrc || echo "/home/ubuntu/.mailrc not set up."
	gpg -d stage-config.json.asc > stage-config.json
	gpg -d prod-config.json.asc > prod-config.json

# update mozilla-central tree
update:
	( cd ${CENTRAL} ;\
	hg pull ;\
	hg update ;\
	cd - )

# update to latest nightly Firefox
nightly:
	rm -rf firefox-nightly
	wget -O firefox-nightly.tar.bz2 'https://download.mozilla.org/?product=firefox-nightly-latest-ssl&os=linux64&lang=en-US'
	tar xjf firefox-nightly.tar.bz2
	mv -i firefox firefox-nightly

prod:
	./run-prod ${PWD}/firefox-nightly/firefox

stage:
	./run-stage ${PWD}/firefox-nightly/firefox

