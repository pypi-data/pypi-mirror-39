import hashlib
import json
from collections import OrderedDict

from rox.core.consts import property_type


class BUID:
    BUID_GENERATORS = [
        property_type.PLATFORM,
        property_type.APP_KEY,
        property_type.LIB_VERSION,
        property_type.API_VERSION,
        property_type.CUSTOM_PROPERTIES,
        property_type.FEATURE_FLAGS,
        property_type.REMOTE_VARIABLES
    ]

    def __init__(self, sdk_settings, device_properties, flag_repository, custom_property_repository):
        self.sdk_settings = sdk_settings
        self.device_properties = device_properties
        self.flag_repository = flag_repository
        self.custom_property_repository = custom_property_repository
        self.buid = None

    def get_value(self):
        properties = self.device_properties.get_all_properties()
        values = []
        for pt in BUID.BUID_GENERATORS:
            if pt.name in properties:
                values.append(properties[pt.name])

        values.append(self.serialize_feature_flags())
        values.append(self.serialize_custom_properties())

        value_bytes = '|'.join(values).encode('utf-8')
        m = hashlib.md5()
        m.update(value_bytes)
        hash = m.hexdigest()

        self.buid = hash.upper()
        return self.buid

    def get_query_string_parts(self):
        generators = [pt.name for pt in BUID.BUID_GENERATORS]

        return {
            property_type.BUID.name: self.get_value(),
            property_type.BUID_GENERATORS_LIST.name: ','.join(generators),
            property_type.FEATURE_FLAGS.name: self.serialize_feature_flags(),
            property_type.REMOTE_VARIABLES.name: '[]',
            property_type.CUSTOM_PROPERTIES.name: self.serialize_custom_properties(),
        }

    def serialize_feature_flags(self):
        flags = []
        for v in self.flag_repository.get_all_flags().values():
            f = OrderedDict()
            f['name'] = v.name
            f['defaultValue'] = v.default_value
            f['options'] = v.options
            flags.append(f)
        return json.dumps(flags, separators=(',', ':'))

    def serialize_custom_properties(self):
        properties = []
        for v in self.custom_property_repository.get_all_custom_properties().values():
            p = OrderedDict()
            p['name'] = v.name
            p['type'] = v.type.type
            p['externalType'] = v.type.external_type
            properties.append(p)
        return json.dumps(properties, separators=(',', ':'))

    def __str__(self):
        return self.buid
