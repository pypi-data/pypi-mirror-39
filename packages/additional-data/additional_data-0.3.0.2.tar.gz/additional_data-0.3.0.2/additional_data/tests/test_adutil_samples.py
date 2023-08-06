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
from adxml import Additional_data_xml
from additional_data import PDF_Manipulator
import additional_data_util
import subprocess

class TestClass(object):
    def test_adutil_extract(self):
        import os
        import codecs
        if os.path.exists('ZUGFeRD-invoice.xml'):
            os.remove('ZUGFeRD-invoice.xml')
        print( os.getcwd() )
        additional_data_util.main(['../../ZUGFeRD_1p0_EXTENDED_Warenrechnung.pdf'])
        assert os.path.exists('ZUGFeRD-invoice.xml')
        extracted = codecs.open('ZUGFeRD-invoice.xml','r','utf-8').read()
        original = codecs.open('../../ZUGFeRD-invoice.orig.xml','r','utf-8').read()
        assert extracted == original
        
    def test_ad_create_and_adutil_attach(self):
        from lxml import etree
        import os
        import shutil
        # create the xml
        my_xml = Additional_data_xml(schema_identifier="http://4s4u.de/additional_data/adcollection/base_all_1.0")
        my_xml.insert_additional_data("anpos", "123456", "{urn:ferd:CrossIndustryDocument:invoice:1p0}SpecifiedSupplyChainTradeTransaction/{urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:12}IncludedSupplyChainTradeLineItem[2]")
        ps_xml = etree.fromstring("<packstueck><psnr>12345</psnr><psdes>runde grüne Teller</psdes></packstueck>").getroottree()
        my_xml.insert_alternate_data("altname", "der andere Name", "/{urn:ferd:CrossIndustryDocument:invoice:1p0}SpecifiedSupplyChainTradeTransaction/{urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:12}IncludedSupplyChainTradeLineItem[2]")
        my_xml.insert_additional_data("pspos", ps_xml, "/{urn:ferd:CrossIndustryDocument:invoice:1p0}SpecifiedSupplyChainTradeTransaction/{urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:12}IncludedSupplyChainTradeLineItem[2]")
        as_xml = etree.fromstring("<kosten><currency>EUR</currency><amount>1.23</amount></kosten>").getroottree()
        my_xml.insert_additional_data("aspos", as_xml, "{urn:ferd:CrossIndustryDocument:invoice:1p0}SpecifiedSupplyChainTradeTransaction/{urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:12}IncludedSupplyChainTradeLineItem[2]")
        print("is valid against the base schema:", my_xml.check_schema('../../additional_data_base_schema.xsd'))
        print(my_xml.write_ad_to_string(pretty_print=True))
        if os.path.exists('additional_data-logistics-invoice-1.0-unique.xml'):
            os.remove('additional_data-logistics-invoice-1.0-unique.xml')
        my_xml.write_ad_to_file('additional_data-logistics-invoice-1.0-unique.xml')
        shutil.copy('../../ZUGFeRD_1p0_EXTENDED_Warenrechnung.pdf','test.pdf')
        shutil.copy('../../additional_data_base_schema.xsd','test.xsd') 
        additional_data_util.main(['test.pdf','additional_data-logistics-invoice-1.0-unique.xml','test.xsd'])
#         myproc = subprocess.Popen("additional_data_util test.pdf additional_data.logistics-invoice-1.0-unique.xml test.xsd", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#         stdout, stderr = myproc.communicate()
#         assert myproc.returncode == 0
        assert os.path.exists('test.pdf')
        mypdf=PDF_Manipulator('test.pdf')
        assert set(mypdf.toc_files) == set(['ZUGFeRD-invoice.xml', 'additional_data-logistics-invoice-1.0-unique.xml'])
        