from fabric.api import *  # noqa
# import fabric


@task
def setup():
    local("git clone https://github.com/kreamkorokke/msisdn-cli")


@task
def teardown():
    local("rm -fr ./msisdn-cli")
