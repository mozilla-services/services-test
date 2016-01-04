from firefox_puppeteer.testcases.base import FirefoxTestCase
from marionette import BaseMarionetteTestRunner
from marionette.runtests import cli as mn_cli


class ServicesTestRunner(BaseMarionetteTestRunner):
    def __init__(self, **kwargs):
        BaseMarionetteTestRunner.__init__(self, **kwargs)
        self.app = 'fxdesktop'
        self.test_handlers = [FirefoxTestCase]


def cli():
    mn_cli(runner_class=ServicesTestRunner)

if __name__ == '__main__':
    cli()
