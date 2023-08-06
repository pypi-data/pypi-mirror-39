#!/bin/python3
# -*- coding: UTF-8 -*-
#
# MIT License
#
# Copyright (c) 02.05.2018 Andreas Starke
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#=============================================================================
# imports
#=============================================================================
from lxml import etree
from copy import deepcopy
from base64 import b64encode
from PyPDF2.pdf import PdfFileReader, PdfFileWriter
from PyPDF2.generic import DictionaryObject, DecodedStreamObject, \
    NameObject, createStringObject, ArrayObject
import logging
name  = "adx"
#===============================================================================
# logging
#===============================================================================
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('additional_data.Additional_data_xml')
logger.setLevel(logging.INFO)


#=============================================================================
# helper classes
#=============================================================================
class Additional_data_xml:
    #=========================================================================
    # supports creating, reading and writing additional data files
    #=========================================================================
    # holds the additional data xml structure
    ad_xml_tree = None
    # holds the exact additional namespace
    ad_namespace = None
    # optionally holds the structure to be extended - allows for verification of references
    basic_object = None
    
    def __init__(self, ifname=None, schema_identifier=None, boname=None):
        """creates the ad xml tree either empty or based upon file"""
        parser = etree.XMLParser(remove_blank_text=True)
        if ifname is not None:
            self.ad_xml_tree = etree.parse(ifname, parser)
        elif schema_identifier is not None:
            self.ad_xml_tree = etree.fromstring('<adt:additionalOrAlternateData xmlns:adt="' + schema_identifier + '"></adt:additionalOrAlternateData>').getroottree()
            self.ad_namespace = schema_identifier
        else:
            raise Exception("neither infile nor schema id given")
        # basic_object if XML needs to be parsed into element tree
        if boname is not None:
            try:
                self.basic_object = etree.parse(boname, parser)
            except:
                raise Exception("only xml basic objects supported")
        if self.ad_namespace is not None:
            self.set_referenced_data_reference(boname)
            
    def set_referenced_data_reference(self, ref):
        """set a reference on the data object for which we have additional data"""
        if self.ad_xml_tree.find('{' +self.ad_namespace + '}referencedData') is not None:
            self.ad_xml_tree.find('{' +self.ad_namespace + '}referencedData').text = ref
        else:
            new_element = etree.SubElement(self.ad_xml_tree.getroot(), "{" + self.ad_namespace + "}referencedData")
            new_element.set("type", "URI")
            new_element.text = ref
    
    def check_schema(self, sfname='additional_data_base_schema.xsd'):
        """needs the name of the schema file to validate against"""
        parser = etree.XMLParser(remove_blank_text=True)
        ad_schema_tree = etree.parse(sfname, parser)
        ad_schema_obj = etree.XMLSchema(ad_schema_tree)
        try:
            ad_schema_obj.assertValid(self.ad_xml_tree)
            return True
        except Exception as e:
            logger.error(e.args[0])
            return False

    def set_namespace(self, ns):
        """sets the namespace argument"""
        self.ad_namespace = ns

    def insert_additional_xml_data(self, pelem, data):
        """inserts the xml element into the parent"""
        for i in range(0, len(data.getchildren())):
            # construct a deep copy such that childs might be changed on global scope without harm
            own_child = deepcopy(data[i])
            own_child.tag = "{" + self.ad_namespace + "}" + own_child.tag
            pelem.append(own_child)

    def insert_additional_binary_data(self, pelem, data):
        """inserts the data base64 coded"""
        pelem.text = b64encode(data) 
        
    def check_reference_exists(self, ref_type, ref):
        """checks whether referenced element exists - if not raise exception"""
        if ref_type == "XPath":
            if isinstance(self.basic_object, etree._ElementTree):
                if self.basic_object.find(ref) is None:
                    raise Exception("additional data is referring to non existent element")

    def insert_additional_data(self, data_type, data, ref, ref_type="XPath"):
        """insert an additional data element"""
        if self.basic_object is not None:
            self.check_reference_exists(ref_type, ref)
                
        new_element = etree.SubElement(self.ad_xml_tree.getroot(), "{" + self.ad_namespace + "}additionalData")
        new_data_element = etree.SubElement(new_element, "{" + self.ad_namespace + "}data")
        new_ref_element = etree.SubElement(new_element, "{" + self.ad_namespace + "}referencedElement")
        new_data_element.set("type", "{" + self.ad_namespace + "}" + data_type)
        new_ref_element.set("type", ref_type)
        new_ref_element.text = ref
        if isinstance(data, str):             
            new_data_element.text = data
        elif isinstance(data, etree._ElementTree):
            self.insert_additional_xml_data(new_data_element, data.getroot())            
        elif isinstance(data, etree._Element):
            self.insert_additional_xml_data(new_data_element, data)
        elif isinstance(data, bytes):
            self.insert_additional_binary_data(new_data_element, data)
        else:
            raise Exception("invalid data type")
        # find the last position to include additional data
        pos_new = len(self.ad_xml_tree.findall("//{" + self.ad_namespace + "}additionalData")) + len(self.ad_xml_tree.findall("//{" + self.ad_namespace + "}referencedData"))
        self.ad_xml_tree.getroot().insert(pos_new - 1, new_element)

    def insert_alternate_data(self, data_type, data, ref, ref_type="XPath"):
        """insert an alternative data element"""
        new_element = etree.SubElement(self.ad_xml_tree.getroot(), "{" + self.ad_namespace + "}alternateData")
        new_data_element = etree.SubElement(new_element, "{" + self.ad_namespace + "}data")
        new_ref_element = etree.SubElement(new_element, "{" + self.ad_namespace + "}referencedElement")
        new_data_element.set("type", "{" + self.ad_namespace + "}" + data_type)
        new_ref_element.set("type", ref_type)
        new_ref_element.text = ref
        if isinstance(data, str):             
            new_data_element.text = data
        elif isinstance(data, etree._ElementTree):
            self.insert_additional_xml_data(new_data_element, data.getroot())            
        elif isinstance(data, etree._Element):
            self.insert_additional_xml_data(new_data_element, data)
        elif isinstance(data, bytes):
            self.insert_additional_binary_data(new_data_element, data)
        else:
            raise Exception("invalid data type")
        # find the last position to include additional data
        self.ad_xml_tree.getroot().append(new_element)

    def read_ad_from_string(self, istring):
        """reads the ad xml tree from the given string"""
        self.ad_xml_tree = etree.fromstring(istring)

    def read_ad_from_file(self, ifname):
        """reads the xml tree from a file"""
        parser = etree.XMLParser(remove_blank_text=True)
        self.ad_xml_tree = etree.parse(ifname, parser)

    def write_ad_to_string(self, encoding="utf-8", pretty_print=False):
        """returns the ad xml tree as a string - see python documentation for valid/available string encodings"""
        return etree.tostring(self.ad_xml_tree.getroot(), pretty_print=pretty_print).decode(encoding)

    def write_ad_to_file(self, ofname):
        """writes the xml tree to the file"""
        outfile = open(ofname, "wb")
        self.ad_xml_tree.write(outfile, pretty_print=True)
        outfile.flush()
        outfile.close()
