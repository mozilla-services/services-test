from marionette import BaseMarionetteTestRunner
from marionette.runtests import cli


class ServicesTestRunner(BaseMarionetteTestRunner):
    def __init__(self, **kwargs):
        BaseMarionetteTestRunner.__init__(self, **kwargs)
        self.app = 'fxdesktop'

if __name__ == '__main__':
    cli()
