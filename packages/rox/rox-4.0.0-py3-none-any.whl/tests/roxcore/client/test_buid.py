import json
import unittest
from collections import OrderedDict

from rox.core.client.buid import BUID
from rox.core.custom_properties.custom_property import CustomProperty
from rox.core.custom_properties.custom_property_type import CustomPropertyType
from rox.core.entities.flag import Flag

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock


class BUIDTests(unittest.TestCase):
    def test_will_generate_correct_md5_value(self):
        flag = Flag()
        flag.set_name('flag1')

        flag_repo = Mock()
        flag_repo.get_all_flags.return_value = OrderedDict({'flag1': flag})

        cp = CustomProperty('prop1', CustomPropertyType.STRING, '123')

        cp_repo = Mock()
        cp_repo.get_all_custom_properties.return_value = OrderedDict({'prop1': cp})

        sdk_settings = Mock()

        device_props = Mock()
        device_props.get_all_properties.return_value = {
            'app_key': '123',
            'api_version': '4.0.0',
            'cache_miss_url': 'harta'
        }

        buid = BUID(sdk_settings, device_props, flag_repo, cp_repo)

        self.assertEqual('5512E154362F3127B817C913A3B286CF', buid.get_value())

    def test_will_generate_correct_md5_value_check_order(self):
        flag1 = Flag()
        flag1.set_name('flag1')

        flag2 = Flag()
        flag2.set_name('flag2')

        flag_repo = Mock()
        flags = OrderedDict()
        flags['flag2'] = flag2
        flags['flag1'] = flag1
        flag_repo.get_all_flags.return_value = flags

        cp1 = CustomProperty('prop1', CustomPropertyType.STRING, '123')
        cp2 = CustomProperty('prop2', CustomPropertyType.STRING, '456')

        cp_repo = Mock()
        props = OrderedDict()
        props['prop2'] = cp2
        props['prop1'] = cp1
        cp_repo.get_all_custom_properties.return_value = props

        sdk_settings = Mock()

        device_props = Mock()
        device_props.get_all_properties.return_value = {
            'app_key': '123',
            'api_version': '4.0.0',
            'cache_miss_url': 'harta'
        }

        buid = BUID(sdk_settings, device_props, flag_repo, cp_repo)

        self.assertEqual('98A097D6EF589A2959640399513152C9', buid.get_value())

    def test_will_serialize_flags(self):
        flag = Flag()
        flag.set_name('flag1')

        flag_repo = Mock()
        flag_repo.get_all_flags.return_value = {'flag1': flag}

        buid = BUID(None, None, flag_repo, None)

        obj = json.loads(buid.serialize_feature_flags())[0]

        self.assertEqual('flag1', obj['name'])
        self.assertEqual('false', obj['defaultValue'])
        self.assertEqual('false', obj['options'][0])
        self.assertEqual('true', obj['options'][1])

    def test_will_serialize_props(self):
        cp = CustomProperty('prop1', CustomPropertyType.STRING, '123')

        cp_repo = Mock()
        cp_repo.get_all_custom_properties.return_value = {'prop1': cp}

        buid = BUID(None, None, None, cp_repo)

        obj = json.loads(buid.serialize_custom_properties())[0]

        self.assertEqual('prop1', obj['name'])
        self.assertEqual(CustomPropertyType.STRING.type, obj['type'])
        self.assertEqual(CustomPropertyType.STRING.external_type, obj['externalType'])
