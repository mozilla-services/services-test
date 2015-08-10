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
  apt-get install -y software-properties-common && \
  apt-get install -y byobu curl git htop man unzip vim wget && \
  apt-get install -y python python-dev python-pip && \
  apt-get install -y nodejs npm && \
  pip install virtualenv jsonschema functools32 && \
  rm -rf /var/lib/apt/lists/* && \
  git clone https://github.com/mozilla-services/services-test

WORKDIR /services-test

# add your "docker" private key pair
ADD ~/.ssh/docker /
RUN \
  chmod 600 /docker && \
  echo "IdentityFile /docker" >> /etc/ssh/ssh_config \

# Expose ports needed for tests to run
# e.g. EXPOSE 80
