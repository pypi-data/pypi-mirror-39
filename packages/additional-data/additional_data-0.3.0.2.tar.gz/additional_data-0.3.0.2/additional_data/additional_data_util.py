#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#
# Copyright 02.05.2018 Andreas Starke
#
#===============================================================================
# CLI for manipulating pdf and additional data extension 
# files
#===============================================================================

#===============================================================================
# imports
#===============================================================================
from optparse import OptionParser
from additional_data.pdfmanipulator import PDF_Manipulator
from os import path
import logging
import sys
#===============================================================================
# logging
#===============================================================================
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('additional-data-util')
logger.setLevel(logging.INFO)
    
def main(unparsed_args=sys.argv[1:]):
    #===========================================================================
    # started directly - CLI invoked
    #===========================================================================
    cli_parser = OptionParser("usage: %prog [options] pdf [adxml-xml, schema-xsd]\nif only the pdf argument is given embedded xmls will be extracted\notherwise the adxml-xml and schema-xsd will be embedded additionally")
    cli_parser.add_option("-l", "--logo", dest="logo",
                           default=None, 
                           help="file path to the logo to be watermarked onto the pdf - only makes sense if you are embedding an xml")
    cli_parser.add_option("-p", "--logo-position", dest="position", default="5x5",
                           help="tuple of x,y coordinates for the logo")
    (options, args) = cli_parser.parse_args(unparsed_args)
    logo_filename = options.logo
    logo_position = options.position
            
    # verify that     
    if len(args)==0:
        cli_parser.error("no arguments given")
    elif len(args)==1:
        # extract all interesting XML
        pdf_manipulator = PDF_Manipulator(args[0])
        for this_embedded_file in pdf_manipulator.toc_files:
            extracted_contents = pdf_manipulator.extract_embedded_file(this_embedded_file)
            if path.exists(this_embedded_file):
                logger.error("will not overwrite existing file " + this_embedded_file)
                sys.exit(2)
            open(this_embedded_file, "wb").write(extracted_contents)
            print(this_embedded_file)
    elif len(args)==3:
        # embed the addtional data XML in the pdf
        pdf_manipulator = PDF_Manipulator(args[0])
        xml_filename = args[1]
        sfilename = args[2]
        # if a logo was given watermark it on the pdf
        pdf_manipulator.embed_ad_xml(xml_filename,sfilename,logo_filename,logo_position)
    else:
        cli_parser.error("incorrect number of arguments")

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
