import unittest

from concurrent import futures

from rox.core.core import Core

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock


class CoreTests(unittest.TestCase):
    def test_will_check_core_setup_when_options_with_roxy(self):
        sdk_settings = Mock()
        device_props = Mock()
        device_props.rollout_key = 'rollout_key'
        rox_options = Mock()
        rox_options.roxy_url = 'http://site.com'
        rox_options.fetch_interval = 30

        c = Core()
        task = c.setup(sdk_settings, device_props, rox_options)
        cancel_event = task.result()
        cancel_event.set()

    def test_will_check_core_setup_when_no_options(self):
        sdk_settings = Mock()
        device_props = Mock()
        device_props.rollout_key = 'rollout_key'

        c = Core()
        task = c.setup(sdk_settings, device_props, None)
        cancel_event = task.result()
        cancel_event.set()
