from fabric.api import task, local


@task
def setup():
    local("git clone https://github.com/kreamkorokke/msisdn-cli")


@task
def teardown():
    local("rm -fr ./msisdn-cli")
