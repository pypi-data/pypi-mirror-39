from rox.core.network.configuration_fetcher_base import ConfigurationFetcherBase
from rox.core.network.configuration_result import ConfigurationSource, ConfigurationFetchResult


class ConfigurationFetcherRoxy(ConfigurationFetcherBase):
    def fetch_from_roxy(self):
        return self.request.send_get(self.request_configuration_builder.build_for_roxy())

    def fetch(self):
        source = ConfigurationSource.ROXY
        try:
            fetch_roxy = self.fetch_from_roxy()

            if self.is_success_status_code(fetch_roxy.status_code):
                return ConfigurationFetchResult(fetch_roxy.text, source)
            else:
                self.write_fetch_error_to_log_and_invoke_fetch_handler(source, fetch_roxy)
        except Exception as ex:
            self.write_fetch_exception_to_log_and_invoke_fetch_handler(source, ex)

        return None
