from fabric.api import *
import fabric

@task
def setup():
    local("git clone https://github.com/kreamkorokke/msisdn-cli")

@task
def teardown():
    local("rm -fr ./msisdn-cli")
