# TODO: Download and install latest Firefox browser for Ubuntu.
# wget https://ftp.mozilla.org/pub/mozilla.org/firefox/releases/latest/linux-x86_64/en-US/firefox-38.0.5.tar.bz2
# tar -xjvf *.bz2 -C /home/ubuntu

# TODO: karl optimization for downloading latest version without needing to hardcode version numbers. :+1:
# LATEST_DMG=$(curl -s ftp://ftp.mozilla.org/pub/mozilla.org/firefox/nightly/latest-mozilla-central/ | fgrep en-US.mac.dmg | awk '{print $9}'
# curl -# -C - -o $DIR'/LatestNightly.dmg' "ftp://ftp.mozilla.org/pub/mozilla.org/firefox/nightly/latest-mozilla-central/$LATEST_DMG"

npm install
