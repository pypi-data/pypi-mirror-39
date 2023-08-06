#!/bin/python3
# -*- coding: UTF-8 -*-
#
#Copyright 06.07.2018 Andreas Starke
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
import pytest
from adxml import Additional_data_xml
import shutil    
@pytest.fixture
def empty_logistics_ad():
    return Additional_data_xml(schema_identifier="http://4s4u.de/additional_data/adcollection/base_all_1.0")

@pytest.fixture
def invalid_boname():
    """returns a non-xml filename that fails the parsing"""
    return "test.pdf."
    
class TestClass(object):
    
    def test_ad_init_from_file(self):
        shutil.copy('../../additional-data-logistics-1.0.xml', 'additional-data-logistics-1.0.xml')
        myad = Additional_data_xml('additional-data-logistics-1.0.xml')
        assert isinstance(myad, Additional_data_xml)
        
    def test_ad_init_empty(self):
        myad = Additional_data_xml(schema_identifier="http://4s4u.de/additional_data/adcollection/base_all_1.0")
        assert isinstance(myad, Additional_data_xml)
        
    def test_ad_init_bo_invalid(self, invalid_boname):
        with pytest.raises(Exception):
            Additional_data_xml(schema_identifier="http://4s4u.de/additional_data/adcollection/base_all_1.0", boname=invalid_boname)
            
    def test_check_reference(self, empty_logistics_ad):
        assert empty_logistics_ad.ad_namespace == "http://4s4u.de/additional_data/adcollection/base_all_1.0"
        
    def test_check_schema(self):
        shutil.copy('../../additional-data-logistics-1.0.xml', 'additional-data-logistics-1.0.xml')
        shutil.copy('../../additional_data_base_schema.xsd', 'additional_data_base_schema.xsd')
        myad = Additional_data_xml('additional-data-logistics-1.0.xml')
        assert myad.check_schema('additional_data_base_schema.xsd')
        
    def test_check_schema_fail(self):
        shutil.copy('../../additional-data-logistics-fail.xml', 'additional-data-logistics-fail.xml')
        myad = Additional_data_xml('additional-data-logistics-fail.xml')
        assert not myad.check_schema('additional_data_base_schema.xsd')