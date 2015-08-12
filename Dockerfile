#
# Services Test Dockerfile
#
# https://github.com/mozilla-services/services-test
#

FROM ubuntu:14.04

# Install test dependencies.
RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y build-essential && \
  apt-get install -y software-properties-common

# Install vnc, xvfb in order to create a 'fake' display and firefox
RUN \
  apt-get install -y x11vnc xvfb firefox && \
  mkdir ~/.vnc && \
  x11vnc -storepasswd 1234 ~/.vnc/passwd

RUN \
  add-apt-repository ppa:chris-lea/node.js && \
  apt-get install -y nodejs-legacy npm

RUN \
  apt-get install -y byobu curl git htop man unzip vim wget && \
  apt-get install -y python python-dev python-pip && \
  pip install virtualenv jsonschema functools32 && \
  rm -rf /var/lib/apt/lists/* && \
  git clone https://github.com/mozilla-services/services-test

WORKDIR /services-test

# add your "docker" private key pair
# ADD docker /
RUN \
  # chmod 600 /docker && \
  mkdir /root/.ssh/ && \
  echo "IdentityFile /root/.ssh/id_rsa" >> /etc/ssh/ssh_config \

# Expose ports needed for tests to run
# e.g. EXPOSE 80
