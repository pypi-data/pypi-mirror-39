import unittest

from rox.core.configuration.configuration_fetched_invoker import ConfigurationFetchedInvoker
from rox.core.network.configuration_fetcher_roxy import ConfigurationFetcherRoxy
from rox.core.network.configuration_result import ConfigurationSource
from rox.core.network.request import RequestData

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock


class ConfigurationFetcherRoxyTests(unittest.TestCase):
    def test_will_return_cdn_data_when_successful(self):
        response = Mock()
        response.status_code = 200
        response.text = 'harti'

        request = Mock()
        request.send_get.return_value = response

        request_data = RequestData('harta.com', None)
        request_builder = Mock()
        request_builder.build_for_roxy.return_value = request_data

        conf_fetch_invoker = TestConfigurationFetchedInvoker()
        conf_fetcher = ConfigurationFetcherRoxy(request_builder, request, conf_fetch_invoker)
        result = conf_fetcher.fetch()

        self.assertEqual('harti', result.data)
        self.assertEqual(ConfigurationSource.ROXY, result.source)
        self.assertEqual(0, conf_fetch_invoker.number_of_times_called)

    def test_will_return_null_when_roxy_fails_with_exception(self):
        request_data = RequestData('harta.com', None)

        response = Mock()
        response.status_code = 404

        request = Mock()
        request.send_get.return_value = response

        request_builder = Mock()
        request_builder.build_for_roxy.return_value = request_data

        conf_fetch_invoker = TestConfigurationFetchedInvoker()
        conf_fetcher = ConfigurationFetcherRoxy(request_builder, request, conf_fetch_invoker)
        result = conf_fetcher.fetch()

        self.assertIsNone(result)
        self.assertEqual(1, conf_fetch_invoker.number_of_times_called)

    def test_will_return_null_when_roxy_fails_with_http_status(self):
        request_data = RequestData('harta.com', None)

        def send_get(data):
            raise Exception('not found')

        request = Mock()
        request.send_get = send_get

        request_builder = Mock()
        request_builder.build_for_roxy.return_value = request_data

        conf_fetch_invoker = TestConfigurationFetchedInvoker()
        conf_fetcher = ConfigurationFetcherRoxy(request_builder, request, conf_fetch_invoker)
        result = conf_fetcher.fetch()

        self.assertIsNone(result)
        self.assertEqual(1, conf_fetch_invoker.number_of_times_called)


class TestConfigurationFetchedInvoker:
    def __init__(self):
        self.cfi = ConfigurationFetchedInvoker()
        self.cfi.register_configuration_fetched_handler(self.on_configuration_fetched)
        self.number_of_times_called = 0

    def invoke(self, fetcher_status, creation_date, has_changes):
        self.cfi.invoke(fetcher_status, creation_date, has_changes)

    def invoke_error(self, error_details):
        self.cfi.invoke_error(error_details)

    def on_configuration_fetched(self, e):
        self.number_of_times_called += 1
