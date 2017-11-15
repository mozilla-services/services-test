
# directory containing a recent hg checkout of mozilla-central
CENTRAL=/mnt/extra/mozilla-central

.PHONY: cron setup update nightly stage prod

# cron setup
# might call this "install" instead -- it needs sudo.
# so, "sudo make cron"
cron:
	cp -i cron.hourly/* /etc/cron.hourly/
	cp -i cron.daily/*  /etc/cron.daily/

# The part of setup that doesn't need root
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

