from requests import status_codes

from rox.core.network.configuration_fetcher_base import ConfigurationFetcherBase
from rox.core.network.configuration_result import ConfigurationSource, ConfigurationFetchResult


class ConfigurationFetcher(ConfigurationFetcherBase):
    def fetch(self):
        source = ConfigurationSource.CDN
        try:
            fetch_result = self.fetch_from_cdn()

            if self.is_success_status_code(fetch_result.status_code):
                return ConfigurationFetchResult(fetch_result.text, source)

            if fetch_result.status_code in (status_codes.codes.forbidden, status_codes.codes.not_found):
                self.write_fetch_error_to_log_and_invoke_fetch_handler(source, fetch_result, raise_configuration_handler=False, next_source=ConfigurationSource.API)
                source = ConfigurationSource.API

                fetch_result = self.fetch_from_api()
                if self.is_success_status_code(fetch_result.status_code):
                    return ConfigurationFetchResult(fetch_result.text, source)

            self.write_fetch_error_to_log_and_invoke_fetch_handler(source, fetch_result)
        except Exception as ex:
            self.write_fetch_exception_to_log_and_invoke_fetch_handler(source, ex)

        return None

    def fetch_from_cdn(self):
        return self.request.send_get(self.request_configuration_builder.build_for_cdn())

    def fetch_from_api(self):
        return self.request.send_get(self.request_configuration_builder.build_for_api())
