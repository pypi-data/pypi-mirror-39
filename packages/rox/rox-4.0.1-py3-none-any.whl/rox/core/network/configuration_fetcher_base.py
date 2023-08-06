from abc import abstractmethod

from rox.core.configuration.configuration_fetched_invoker import FetcherError
from rox.core.logging.logging import Logging


class ConfigurationFetcherBase:
    def __init__(self, request_configuration_builder, request, configuration_fetched_invoker):
        self.request_configuration_builder = request_configuration_builder
        self.request = request
        self.configuration_fetched_invoker = configuration_fetched_invoker

    def write_fetch_error_to_log_and_invoke_fetch_handler(self, source, response, raise_configuration_handler=True, next_source=None):
        retry_msg = '' if next_source is None else 'Trying from %s. ' % next_source

        Logging.get_logger().debug('Failed to fetch from %s. %shttp error code: %s' % (source, retry_msg, response.status_code))

        if raise_configuration_handler:
            self.configuration_fetched_invoker.invoke_error(FetcherError.NETWORK_ERROR)

    def write_fetch_exception_to_log_and_invoke_fetch_handler(self, source, ex):
        Logging.get_logger().error('Failed to fetch configuration. Source: %s. Ex: %s' % (source, ex))
        self.configuration_fetched_invoker.invoke_error(FetcherError.NETWORK_ERROR)

    @abstractmethod
    def fetch(self):
        pass

    def is_success_status_code(self, status_code):
        return 200 <= status_code < 300
