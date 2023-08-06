import unittest

from rox.core.configuration.configuration_fetched_invoker import ConfigurationFetchedInvoker
from rox.core.network.configuration_fetcher import ConfigurationFetcher
from rox.core.network.configuration_result import ConfigurationSource
from rox.core.network.request import RequestData

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock


class ConfigurationFetcherTests(unittest.TestCase):
    def test_will_return_cdn_data_when_successful(self):
        response = Mock()
        response.status_code = 200
        response.text = 'harti'

        request = Mock()
        request.send_get.return_value = response

        request_data = RequestData('harta.com', None)
        request_builder = Mock()
        request_builder.build_for_cdn.return_value = request_data

        conf_fetch_invoker = TestConfigurationFetchedInvoker()
        conf_fetcher = ConfigurationFetcher(request_builder, request, conf_fetch_invoker)
        result = conf_fetcher.fetch()

        self.assertEqual('harti', result.data)
        self.assertEqual(ConfigurationSource.CDN, result.source)
        self.assertEqual(0, conf_fetch_invoker.number_of_times_called)

    def test_will_return_null_when_cdn_fails_with_exception(self):
        request_data_cdn = RequestData('harta.com', None)
        request_data_api = RequestData('harta.com', None)

        response = Mock()
        response.status_code = 200
        response.text = 'harto'

        def send_get(request_data):
            if request_data == request_data_cdn:
                raise Exception('not found')
            elif request_data == request_data_api:
                return response

        request = Mock()
        request.send_get = send_get

        request_builder = Mock()
        request_builder.build_for_cdn.return_value = request_data_cdn
        request_builder.build_for_api.return_value = request_data_api

        conf_fetch_invoker = TestConfigurationFetchedInvoker()
        conf_fetcher = ConfigurationFetcher(request_builder, request, conf_fetch_invoker)
        result = conf_fetcher.fetch()

        self.assertIsNone(result)
        self.assertEqual(1, conf_fetch_invoker.number_of_times_called)

    def test_will_return_null_when_cdn_fails_404_api_with_exception(self):
        request_data_cdn = RequestData('harta.com', None)
        request_data_api = RequestData('harta.com', None)

        response = Mock()
        response.status_code = 404

        def send_get(request_data):
            if request_data == request_data_cdn:
                return response
            elif request_data == request_data_api:
                raise Exception('exception')

        request = Mock()
        request.send_get = send_get

        request_builder = Mock()
        request_builder.build_for_cdn.return_value = request_data_cdn
        request_builder.build_for_api.return_value = request_data_api

        conf_fetch_invoker = TestConfigurationFetchedInvoker()
        conf_fetcher = ConfigurationFetcher(request_builder, request, conf_fetch_invoker)
        result = conf_fetcher.fetch()

        self.assertIsNone(result)
        self.assertEqual(1, conf_fetch_invoker.number_of_times_called)

    def test_will_return_api_data_when_cdn_fails_404_api_ok(self):
        request_data_cdn = RequestData('harta.com', None)
        request_data_api = RequestData('harta.com', None)

        response = Mock()
        response.status_code = 200
        response.text = 'harto'

        response_cdn = Mock()
        response_cdn.status_code = 404

        def send_get(request_data):
            if request_data == request_data_cdn:
                return response_cdn
            elif request_data == request_data_api:
                return response

        request = Mock()
        request.send_get = send_get

        request_builder = Mock()
        request_builder.build_for_cdn.return_value = request_data_cdn
        request_builder.build_for_api.return_value = request_data_api

        conf_fetch_invoker = TestConfigurationFetchedInvoker()
        conf_fetcher = ConfigurationFetcher(request_builder, request, conf_fetch_invoker)
        result = conf_fetcher.fetch()

        self.assertEqual('harto', result.data)
        self.assertEqual(ConfigurationSource.API, result.source)
        self.assertEqual(0, conf_fetch_invoker.number_of_times_called)

    def test_will_return_null_data_when_both_not_found(self):
        request_data_cdn = RequestData('harta.com', None)
        request_data_api = RequestData('harta.com', None)

        response = Mock()
        response.status_code = 404

        response_cdn = Mock()
        response_cdn.status_code = 404

        def send_get(request_data):
            if request_data == request_data_cdn:
                return response_cdn
            elif request_data == request_data_api:
                return response

        request = Mock()
        request.send_get = send_get

        request_builder = Mock()
        request_builder.build_for_cdn.return_value = request_data_cdn
        request_builder.build_for_api.return_value = request_data_api

        conf_fetch_invoker = TestConfigurationFetchedInvoker()
        conf_fetcher = ConfigurationFetcher(request_builder, request, conf_fetch_invoker)
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
