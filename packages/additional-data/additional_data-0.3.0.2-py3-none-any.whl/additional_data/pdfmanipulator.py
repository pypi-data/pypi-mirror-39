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
from PyPDF2.pdf import PdfFileReader, PdfFileWriter, PageObject, ContentStream
from PyPDF2.generic import DictionaryObject, DecodedStreamObject, \
    NameObject, createStringObject, ArrayObject
import logging
from additional_data.adxml import Additional_data_xml
from hashlib import md5
from datetime import datetime
from os import path
from lxml import etree
import re
from additional_data import __version__
from reportlab.pdfgen import canvas
from io import BytesIO

#===============================================================================
# logging
#===============================================================================
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('additional_data.PDF_Manipulator')
logger.setLevel(logging.INFO)

__metadata_xmp_str__ = """<!-- Copyright Andreas Starke 2018
This XMP schema specifies XMP entries for the included additional-data based on PDF/A-3. The following properties
of the custom schema are used:
Schema name: additional-data Schema
Schema namespace URI: https://www.zugferd-community.net/additional-data/1.0
Preferred schema namespace prefix: adt
Since this schema is beyond the set of predefined XMP 2004 schemas it includes a
description of the custom schema according to the PDF/A requirements.
-->
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
<!-- XMP extension schema container for the additional data schema -->
<rdf:Description rdf:about=""
xmlns:pdfaExtension="http://www.aiim.org/pdfa/ns/extension/"
xmlns:pdfaSchema="http://www.aiim.org/pdfa/ns/schema#"
xmlns:pdfaProperty="http://www.aiim.org/pdfa/ns/property#" >
<!-- Container for all embedded extension schema descriptions -->
<pdfaExtension:schemas>
<rdf:Bag>
<rdf:li rdf:parseType="Resource">
<!-- Optional description of schema -->
<pdfaSchema:schema>additional-data PDFA Extension Schema</pdfaSchema:schema>
<!-- Schema namespace URI -->
<pdfaSchema:namespaceURI>https://www.zugferd-community.net/additional-data/1.0#</pdfaSchema:namespaceURI>
<!-- Preferred schema namespace prefix -->
<pdfaSchema:prefix>adt</pdfaSchema:prefix>
<!-- Description of schema properties -->
<pdfaSchema:property>
<rdf:Seq> 
<rdf:li rdf:parseType="Resource">
<pdfaProperty:name>DocumentFileName</pdfaProperty:name>
<pdfaProperty:valueType>Text</pdfaProperty:valueType>
<pdfaProperty:category>external</pdfaProperty:category>
<pdfaProperty:description>name of the embedded additional data XML file</pdfaProperty:description>
</rdf:li>
<rdf:li rdf:parseType="Resource">
<pdfaProperty:name>DocumentType</pdfaProperty:name>
<pdfaProperty:valueType>Text</pdfaProperty:valueType>
<pdfaProperty:category>external</pdfaProperty:category>
<pdfaProperty:description>the actual type of additional data</pdfaProperty:description>
</rdf:li>
<rdf:li rdf:parseType="Resource">
<pdfaProperty:name>Version</pdfaProperty:name>
<pdfaProperty:valueType>Text</pdfaProperty:valueType>
<pdfaProperty:category>external</pdfaProperty:category>
<pdfaProperty:description>The actual version of the additional data XML schema</pdfaProperty:description>
</rdf:li>
</rdf:Seq>
</pdfaSchema:property>
</rdf:li>
</rdf:Bag>
</pdfaExtension:schemas>
</rdf:Description>
</rdf:RDF>
"""


    
class PDF_Manipulator():
    #===========================================================================
    # supports extracting or embedding xml files in pdf
    #===========================================================================
    pdf_filename = None
    pdf = None
    pdf_creator_metadata = None
    toc_files = None
    
    def __init__(self, pdf_filename):
        """initialize with file data"""
        self.pdf_filename = pdf_filename
        if self.pdf_filename is not None:
            self.pdf = PdfFileReader(self.pdf_filename)
        # populate the toc
        self.toc_files = self.get_toc()
        # initialize creator metadata
        self.pdf_creator_metadata = {
            'author': 'unknown',
            'keywords': 'additional-data',
            'title': 'additional-data.xml',
            'subject': 'additional-data extending information of the base reference file',
            } 
            
    def get_toc(self):
        """get the table of contents of embedded files"""
        toc = []
        
        try:
            pdf_root = self.pdf.trailer['/Root']
            if '/Names' not in pdf_root:
                return toc
            elif '/EmbeddedFiles' not in pdf_root['/Names']:
                return toc
            embedded_files = pdf_root['/Names']['/EmbeddedFiles']['/Names']
            # if it's not odd then the contents table is damaged 
            if len(embedded_files) % 2 != 0:
                raise Exception("pdf embedded file contents table is broken")
            for i in range(0, len(embedded_files), 2):
                toc.append(embedded_files[i])
        except:
            logger.error('No valid Names array found in PDF')
            return toc
        
        return toc
        
    def extract_embedded_file(self, filename=None):
        """returns the binary contents of the referenced stream object"""
        # get that thingy
        pdf_root = self.pdf.trailer['/Root']
        embedded_files = pdf_root['/Names']['/EmbeddedFiles']['/Names']
        for i in range(0, len(embedded_files), 2):
            if embedded_files[i] == filename:
                logger.debug("extracting: %s", embedded_files[i])
                return embedded_files[i + 1].getObject()['/EF']['/F'].getData()    
    
    def envelope_metadata_str(self, mstr):
        """envelopes a metadata string for streaming with an xpacket
        XMP Specification Part 3 - 2.6.1 PDF
        @mstr: is expected to be utf-8 encoded"""
        # standard envelope
        header = u'<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?>'.encode(
            'utf-8')
        footer = u'<?xpacket end="w"?>'.encode('utf-8')
        return header + mstr + footer
    
    def get_metadata_xml_str(self, ad_filename):
        """construct the metadata stream data"""
        # this might still be a little bit rough around the edges...
        # building namespace maps helps a lot with etree elements
        ns_xml = '{http://www.w3.org/XML/1998/namespace}'
        nsmap_dc = {'dc': 'http://purl.org/dc/elements/1.1/'}
        ns_dc = '{%s}' % nsmap_dc['dc']
        nsmap_x = {'x': 'adobe:ns:meta/'}
        ns_x = '{%s}' % nsmap_x['x']
        nsmap_rdf = {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}
        ns_rdf = '{%s}' % nsmap_rdf['rdf']
        nsmap_pdf = {'pdf': 'http://ns.adobe.com/pdf/1.3/'}
        ns_pdf = '{%s}' % nsmap_pdf['pdf']
        nsmap_xmp = {'xmp': 'http://ns.adobe.com/xap/1.0/'}
        ns_xmp = '{%s}' % nsmap_xmp['xmp']
        nsmap_pdfaid = {'pdfaid': 'http://www.aiim.org/pdfa/ns/id/'}
        ns_pdfaid = '{%s}' % nsmap_pdfaid['pdfaid']
        nsmap_adt = {'adt': 'https://www.zugferd-community.net/additional-data/1.0#'}
        ns_adt = '{%s}' % nsmap_adt['adt']
        
        root = etree.Element(ns_x + 'xmpmeta', nsmap=nsmap_x)
        rdf = etree.SubElement(
            root, ns_rdf + 'RDF', nsmap=nsmap_rdf)
        desc_pdfaid = etree.SubElement(
            rdf, ns_rdf + 'Description', nsmap=nsmap_pdfaid)
        desc_pdfaid.set(ns_rdf + 'about', '')
        etree.SubElement(
            desc_pdfaid, ns_pdfaid + 'part').text = '3'
        etree.SubElement(
            desc_pdfaid, ns_pdfaid + 'conformance').text = 'B'
        desc_dc = etree.SubElement(
            rdf, ns_rdf + 'Description', nsmap=nsmap_dc)
        desc_dc.set(ns_rdf + 'about', '')
        dc_title = etree.SubElement(desc_dc, ns_dc + 'title')
        dc_title_alt = etree.SubElement(dc_title, ns_rdf + 'Alt')
        dc_title_alt_li = etree.SubElement(
            dc_title_alt, ns_rdf + 'li')
        dc_title_alt_li.text = self.pdf_creator_metadata.get('title', '')
        dc_title_alt_li.set(ns_xml + 'lang', 'x-default')
        dc_creator = etree.SubElement(desc_dc, ns_dc + 'creator')
        dc_creator_seq = etree.SubElement(dc_creator, ns_rdf + 'Seq')
        etree.SubElement(
            dc_creator_seq, ns_rdf + 'li').text = self.pdf_creator_metadata.get('author', '')
        dc_desc = etree.SubElement(desc_dc, ns_dc + 'description')
        dc_desc_alt = etree.SubElement(dc_desc, ns_rdf + 'Alt')
        dc_desc_alt_li = etree.SubElement(
            dc_desc_alt, ns_rdf + 'li')
        dc_desc_alt_li.text = self.pdf_creator_metadata.get('subject', '')
        dc_desc_alt_li.set(ns_xml + 'lang', 'x-default')
        desc_adobe = etree.SubElement(
            rdf, ns_rdf + 'Description', nsmap=nsmap_pdf)
        desc_adobe.set(ns_rdf + 'about', '')
        producer = etree.SubElement(
            desc_adobe, ns_pdf + 'Producer')
        producer.text = 'PyPDF2'
        desc_xmp = etree.SubElement(
            rdf, ns_rdf + 'Description', nsmap=nsmap_xmp)
        desc_xmp.set(ns_rdf + 'about', '')
        creator = etree.SubElement(
            desc_xmp, ns_xmp + 'CreatorTool')
        creator.text = 'additional-data python package by Andreas Starke'
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')
        etree.SubElement(desc_xmp, ns_xmp + 'CreateDate').text = timestamp
        etree.SubElement(desc_xmp, ns_xmp + 'ModifyDate').text = timestamp
    
        ad_pdfa_ext_schema_root = etree.fromstring(__metadata_xmp_str__).getroottree()  # @UndefinedVariable
        # embed the additional-data extension schema
        ad_pdfa_ext_schema_desc_xpath = ad_pdfa_ext_schema_root.xpath('//rdf:Description', namespaces=nsmap_rdf)
        rdf.append(ad_pdfa_ext_schema_desc_xpath[0])
        # add our description
        ad_desc = etree.SubElement(
            rdf, ns_rdf + 'Description', nsmap=nsmap_adt)
        ad_desc.set(ns_rdf + 'about', '')
        ad_desc.set(ns_adt + 'DocumentFileName', ad_filename)
        description_regex = re.search(r'^additional_data-(.*)-(.*)-([0-9]+\.[0-9])-(.*)\.[xX][mM][lL]$', ad_filename)
        ad_desc.set(ns_adt + 'DocumentType', description_regex.group(2))
        ad_desc.set(ns_adt + 'Version', description_regex.group(3))
    
        # stuff the string into an xpacket
        xml_str = etree.tostring(
            root, pretty_print=True, encoding="utf-8", xml_declaration=False)
        xml_final_str = self.envelope_metadata_str(xml_str)
        logger.debug('metadata XML:')
        logger.debug(xml_final_str)
        return xml_final_str
    
    def clone_attachments_from_reader(self, old, new):
        """clones the attached files from old to new pdf"""
        # copy all attachments and metadata to the new pdf
        old_root = old.trailer['/Root']
        if '/Names' in old_root:
            if '/EmbeddedFiles' not in old_root['/Names']:
                return
        else:
            return
        embedded_files = old_root['/Names']['/EmbeddedFiles']['/Names']
        attached_filespecs_array = []
        embedded_files_dict = []
        for i in range(0, len(embedded_files), 2):
            # we need our own attach function, since the pypdf2 one's is garbage
            att_name = embedded_files[i]
            # att_obj = embedded_files[i+1].getObject()
            att_obj = embedded_files[i + 1].getObject()['/EF']['/F']
            
            file_entry_obj = new._addObject(att_obj)
            # The Filespec entry
            ef_dict = DictionaryObject({
            NameObject("/F"): file_entry_obj,
            NameObject('/UF'): file_entry_obj
            })
            
            for counter, this_fsde in enumerate(old.trailer['/Root']['/AF']):
                if this_fsde.getObject()['/F'] == att_name:
                    # we are copying this one
                    filespec_dict = old.trailer['/Root']['/AF'][counter]
                    break
            # we just have to change the embedded file objects to the ones in the new pdf
            filespec_dict.getObject().update({NameObject('/EF') : ef_dict})
            
            filespec_obj = new._addObject(filespec_dict)
            attached_filespecs_array.append(filespec_obj)
            embedded_files_dict.append(att_name)
            embedded_files_dict.append(filespec_dict)
        # create the entries
        ef_names = DictionaryObject({NameObject("/Names"): ArrayObject(embedded_files_dict)})
        root_names = DictionaryObject({NameObject("/EmbeddedFiles"): ef_names})
        # get the metadata object if there is any
        if '/Metadata' in old_root.keys():
            metadata_xml_str = old_root['/Metadata'].getObject().getData()
            metadata_file_entry = DecodedStreamObject()
            metadata_file_entry.setData(metadata_xml_str)
            metadata_file_entry.update({
                NameObject('/Subtype'): NameObject('/XML'),
                NameObject('/Type'): NameObject('/Metadata')
                })
            metadata_object = new._addObject(metadata_file_entry)
            new._root_object.update({
            NameObject("/AF"): attached_filespecs_array,
            NameObject("/Metadata"): metadata_object,
            NameObject("/Names"): root_names
            })
        else:
            new._root_object.update({
            NameObject("/AF"): attached_filespecs_array,
            NameObject("/Names"): root_names
            })
            
    def clone_output_intents(self, old, new):
        """clones the OutputIntents, which provide a means for
        matching the colour characteristics of a PDF document
        with those of a target output device or production environment"""
        new_output_intents = []
        old_root = old.trailer['/Root']
        if '/OutputIntents' in old_root.keys():
            ori_output_intents = old_root['/OutputIntents']
            logger.debug('output_intents_list=%s', ori_output_intents)
            for ori_output_intent in ori_output_intents:
                ori_output_intent_dict = ori_output_intent.getObject()
                logger.debug('ori_output_intents_dict=%s', ori_output_intent_dict)
                # output_intent dictionaries hold only one stream element that is the Profile
                # all others are strings and names
                dest_output_profile_obj = ori_output_intent_dict['/DestOutputProfile'].getObject()
                dest_output_profile_obj = new._addObject(dest_output_profile_obj)
                ori_output_intent_dict.update({
                    NameObject("/DestOutputProfile"): dest_output_profile_obj
                    })
                logger.debug(ori_output_intent_dict)
                output_intent_obj = new._addObject(ori_output_intent_dict)
                new_output_intents.append(output_intent_obj)
            logger.debug("new_output_intents: %s", new_output_intents)            
            # set the new Array
            new._root_object.update({NameObject("/OutputIntents"): ArrayObject(new_output_intents)})
    
    def embed_ad_xml(self, filename=None, sfilename=None, lfilename=None, lpos=None):
        """combines a lot of the original pdf with the ad-xml"""
        # TODO: check whether this works when inserting 2 ZUGFeRD and 2 additional-data xml (in case of ZF1.0 + facture-X)
        # write that thingy
        ad_xml = Additional_data_xml(ifname=filename)
        if not ad_xml.check_schema(sfilename):
            raise Exception("ad-xml doesn't fit it's schema")
        ad_xml_str = ad_xml.write_ad_to_string('utf-8', True).encode('utf-8')
        new_pdf = PdfFileWriter()
        # it's good habit to mark this PDF as containing binary data by adding a comment with non-ASCIIs directly after
        # the Version Header (which is irrelevant btw.), we declare pdf/a-3b elsewhere
        new_pdf._header = b'%PDF-1.7\r%\xe2\xe3\xcf\xd3\r'
        new_pdf.appendPagesFromReader(self.pdf)
        self.clone_attachments_from_reader(self.pdf, new_pdf)
        pdf_id = self.pdf.trailer.get('/ID')
        logger.debug('original_pdf_id=%s', pdf_id)
        # since we "manipulate" the pdf (debateable if we create a new one), we should change the 2nd part of the ID
        # if we ever change minds and think we create the pdf, we will set both ID parts to our digest 
        ID_part2 = md5(repr(new_pdf).encode('utf-8')).hexdigest()
        if pdf_id:
            new_pdf._ID = pdf_id
            new_pdf._ID[1] = createStringObject(ID_part2)
        else:
            logger.warn('missing out on ID - we did not create this - anyway, we fix it')
            new_pdf._ID = [createStringObject(ID_part2), createStringObject(ID_part2)]

        # create the dictionary object describing the embedded data 
        md5_sum = md5(ad_xml_str).hexdigest()
        md5_sum_str_obj = createStringObject(md5_sum)
        params_dict = DictionaryObject({
            NameObject('/CheckSum'): md5_sum_str_obj,
            NameObject('/ModDate'): createStringObject(datetime.now().strftime("D:%Y%m%d%H%M%S+00'00'")),
            NameObject('/Size'): NameObject(str(len(ad_xml_str)))
            })
        file_entry = DecodedStreamObject()
        file_entry.setData(ad_xml_str)
        file_entry.update({
            NameObject("/Type"): NameObject("/EmbeddedFile"),
            NameObject("/Params"): params_dict,
            NameObject("/Subtype"): NameObject("/text#2Fxml")
            })
        logging.info(file_entry)
        file_entry_obj = new_pdf._addObject(file_entry)
        # The Filespec entry
        ef_dict = DictionaryObject({
            NameObject("/F"): file_entry_obj,
            NameObject('/UF'): file_entry_obj
            })
     
        fname_obj = createStringObject(path.basename(filename))
        filespec_dict = DictionaryObject({
            NameObject("/AFRelationship"): NameObject("/Supplement"),
            NameObject("/Desc"): createStringObject("additional-data"),
            NameObject("/Type"): NameObject("/Filespec"),
            NameObject("/F"): fname_obj,
            NameObject("/EF"): ef_dict,
            NameObject("/UF"): fname_obj
            })
        logger.debug(filespec_dict)
        filespec_obj = new_pdf._addObject(filespec_dict)
        name_arrayobj_cdict = {fname_obj: filespec_obj}
        logger.debug('name_arrayobj_cdict=%s', name_arrayobj_cdict)
        name_arrayobj_content_sort = list(
            sorted(name_arrayobj_cdict.items(), key=lambda x: x[0]))
        logger.debug('name_arrayobj_content_sort=%s', name_arrayobj_content_sort)
        name_arrayobj_content_final = []
        for (fname_obj, filespec_obj) in name_arrayobj_content_sort:
            name_arrayobj_content_final += [fname_obj, filespec_obj]
        logger.debug('name_arrayobj_content_final=%s', name_arrayobj_content_final)
        embedded_files = []
        if '/Names' in new_pdf._root_object:
            if '/EmbeddedFiles' in new_pdf._root_object['/Names']:
                embedded_files = new_pdf._root_object['/Names']['/EmbeddedFiles']['/Names']
        logger.debug("embedded_files: %s", embedded_files)
        embedded_files_names_dict = DictionaryObject({
            NameObject("/Names"): ArrayObject(embedded_files + name_arrayobj_content_final),
            })
        # Then create the entry for the root, as it needs a
        # reference to the Filespec
        embedded_files_dict = DictionaryObject({
            NameObject("/EmbeddedFiles"): embedded_files_names_dict,
            })
        logger.debug("embedded_files_names_dict: %s", embedded_files_names_dict)
        # check if metadata already exists, if so, we only insert our pdf/a extension schema additionally
        # get our string
        metadata_xml_str = self.get_metadata_xml_str(path.basename(filename))
        if '/Metadata' in new_pdf._root_object.keys():
            # in case of ZUGFeRD/factur-x - we need to just insert our pdf/a extension schema here
            metadata_tree = etree.fromstring(new_pdf._root_object['/Metadata'].getObject().getData()).getroottree()
            additional_schema_tree = etree.fromstring(metadata_xml_str).getroottree()
            additional_schema_node = additional_schema_tree.findall('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF/{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description/{http://www.aiim.org/pdfa/ns/extension/}schemas/{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Bag/{http://www.w3.org/1999/02/22-rdf-syntax-ns#}li')[0]
            old_pdfa_extensions = metadata_tree.findall('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF/{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description/{http://www.aiim.org/pdfa/ns/extension/}schemas/{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Bag')
            old_descriptions = metadata_tree.findall('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF')
            our_description = additional_schema_tree.findall('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF/{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description')[-1]            
            if old_pdfa_extensions != []:
                # insert our additional part                
                old_pdfa_extensions[0].append(additional_schema_node)
                old_descriptions[0].append(our_description)
                # serialize to string
                metadata_xml_str = self.envelope_metadata_str(etree.tostring(metadata_tree.getroot(), pretty_print=True, encoding="utf-8", xml_declaration=False))
            else:
                # TODO: safe the other metadata as much as possible - don't just overwrite it
                # this would be a recursive lookup of what exists in the xmpmeta 
                # and construct elements that are missing and fill them with subsets from get_metadata_xml_str 
                # sounds like a refactoring on the metadata methods
                pass
        metadata_file_entry = DecodedStreamObject()
        metadata_file_entry.setData(metadata_xml_str)
        metadata_file_entry.update({
            NameObject('/Subtype'): NameObject('/XML'),
            NameObject('/Type'): NameObject('/Metadata')
            })
        logger.debug(metadata_file_entry)
        metadata_obj = new_pdf._addObject(metadata_file_entry)
        logger.debug(ArrayObject([filespec_obj]))
        # prepend the original values
        old_filespecs = []
        if '/AF' in self.pdf.trailer['/Root']:
            old_filespecs = self.pdf.trailer['/Root']['/AF']
        af_value_obj = new_pdf._addObject(
            ArrayObject(old_filespecs + [ filespec_obj ]))
        # Update the root
        logger.debug({
            NameObject("/AF"): af_value_obj,
            NameObject("/Metadata"): metadata_obj,
            NameObject("/Names"): embedded_files_dict,
            # show attachments when opening PDF
            NameObject("/PageMode"): NameObject("/UseAttachments")
            }) 
        new_pdf._root_object.update({
            NameObject("/AF"): af_value_obj,
            NameObject("/Metadata"): metadata_obj,
            NameObject("/Names"): embedded_files_dict,
            # show attachments when opening PDF
            NameObject("/PageMode"): NameObject("/UseAttachments")
            })
        # if OutputIntents are given - preserve them so that we don't change color schemes
        self.clone_output_intents(self.pdf, new_pdf)
        # setting our metadata, since we crippled this poor file and shall be held responsible
        metadata_txt_dict = {
            '/Author': self.pdf_creator_metadata.get('author', ''),
            '/CreationDate': datetime.now().strftime("D:%Y%m%d%H%M%S+00'00'"),
            '/Creator': 'additional-data lib v%s by Andreas Starke' % __version__,
            '/Keywords': self.pdf_creator_metadata.get('keywords', ''),
            '/ModDate': datetime.now().strftime("D:%Y%m%d%H%M%S+00'00'"),
            '/Subject': self.pdf_creator_metadata.get('subject', ''),
            '/Title': self.pdf_creator_metadata.get('title', '')
            }
        logger.debug(metadata_txt_dict)
        new_pdf.addMetadata(metadata_txt_dict)
        
        # finally we add the logo
        if lfilename is not None:
            lpos_x_str, lpos_y_str = lpos.split("x")
            first_page = new_pdf.getPage(0)
            # create the watermark using reportlab
            wm_flo = BytesIO()
            wm_c = canvas.Canvas(wm_flo)
            wm_c.drawImage(lfilename, int(lpos_x_str), int(lpos_y_str))
            wm_c.save()
            # read the watermark PDF 
            watermark = PdfFileReader(wm_flo)
            first_page.mergePage(watermark.getPage(0))
        
        # persist the new pdf on fs
        if self.pdf_filename:
            with open(self.pdf_filename, 'wb') as outfile:
                new_pdf.write(outfile)
