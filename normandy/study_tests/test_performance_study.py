import sys
import time
from marionette import Marionette
from marionette_driver.addons import Addons

EXTENSION = '/Users/chartjes/mozilla-services/services-test/normandy/x-screen-draw-performance-shield-study-1.xpi'
BASE = 'extensions.@x-screen-draw-performance-shield-study-1'


class TestPerformanceStudy():
    def setup(self):
        try:
            self.client = Marionette(host='localhost', port=2828)
            self.client.start_session()
            self.client.set_pref('general.warnOnAboutConfig', False)
            self.addons = Addons(self.client)
        except:
            sys.exit("Could not find Firefox browser running")

    def test_normal_install(self):
        self.client.set_pref('nglayout.initialpaint.delay', None)
        firstrun = int(time.time())
        addon_id = self.addons.install(EXTENSION)
        variations = [u'ut', u'medium', u'aggressive', u'weak']
        assert self.client.get_pref("%s.variation" % BASE) in variations
        assert self.client.get_pref("%s.firstrun" % BASE) > firstrun
        self.addons.uninstall(addon_id)
        self.client.close()

    def test_ineligible_for_install(self):
        self.client.set_pref('nglayout.initialpaint.delay', 13)
        addon_id = self.addons.install(EXTENSION)

        # The extension should've been uninstalled, so we catch the exception
        # caused when trying to remove an extension that isn't there
        try:
            self.addons.uninstall(addon_id)
            assert False
        except:
            assert True

        # If set to None, it means the extension got removed
        assert self.client.get_pref("%s.variation" % BASE) is None

    def test_second_start(self):
        self.client.set_pref('nglayout.initialpaint.delay', None)
        self.client.set_pref("%s.variaton" % BASE, 'medium')
        addon_id = self.addons.install(EXTENSION)

        assert self.client.get_pref('nglayout.initialpaint.delay') == 50
        self.addons.uninstall(addon_id)
        self.client.close()

    def test_end_of_study(self):
        self.client.set_pref('nglayout.initialpaint.delay', None)
        self.client.set_pref("%s.firstrun" % BASE, 500)
        addon_id = self.addons.install(EXTENSION)

        # The extension should've been uninstalled, so we catch the exception
        # caused when trying to remove an extension that isn't there
        try:
            self.addons.uninstall(addon_id)
            assert False
        except:
            assert True

        self.client.close()

    def test_user_disable(self):
        self.client.set_pref('nglayout.initialpaint.delay', None)
        addon_id = self.addons.install(EXTENSION)
        self.addons.uninstall(addon_id)
        survey_url = self.client.get_url()
        assert survey_url.find("reason=user-ended-study")
        self.client.close()
