FROM stackbrew/debian:testing

RUN \
    apt clean; \
    apt update; \
    apt upgrade -y; \
    apt install -y --fix-missing python-pip python-virtualenv git-core build-essential make; \
    apt install -y --fix-missing python python-dev libssl-dev libffi-dev; \
    git clone https://github.com/mozilla-services/services-test/ /home/services-test; \
    cd /home/services-test; \
    pip install virtualenv; \
    apt-get remove -y -qq git build-essential python-pip python-virtualenv libssl-dev libffi-dev; \
    apt-get autoremove -y -qq; \
    apt-get clean -y; \
    chmod +x /home/services-test/kinto/run;

WORKDIR /home/services-test

# run the test
CMD ./run
