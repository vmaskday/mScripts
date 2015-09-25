#!/usr/bin/python


import sys
from xml.etree import ElementTree as ET
#from elementtree.ElementTree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
import getopt
import os

care_partition = {'system':'a'}

last_prtition   = ""
last_end_sector = 0
SECTOR_LEN = 512

def find_file(filename,search_paths):
#    print "\n\n\tLooking for",filename
#    print "\t"+"-"*40
    for x in search_paths:
        temp = os.path.join(x, filename)
        if os.path.exists(temp):
            return temp
    if os.path.exists(filename):
        return filename
    return None

#def copy_img(input_file,output_file):
#    in_f  = open(input_file,"rb")
#    out_f = open(output_file,"wb")
#    while True:
#        copybuf = in_f.read(512)
#        if not copybuf:
#            break
#        out_f.write(copybuf)
#

def gen_file(in_f,out_f,fill_bytes):
    outf = open(out_f,"a+")
    if in_f != "":
        inf  = open(in_f,"rb")
        outf.write(inf.read())
        inf.close()
    else:
        data = '\0' * fill_bytes
        outf.write(data)
    outf.close()

def create_img(partition,filename,start_sector,end_sector):
    global last_prtition
    global last_end_sector
    global SECTOR_LEN
    if partition != last_prtition :
        last_prtition = partition
        if os.path.exists(partition + ".img"):
            os.remove(partition + ".img")
    else :
        fill_sector = start_sector - last_end_sector
        fill_bytes  = fill_sector * SECTOR_LEN
        gen_file("",partition + ".img",fill_bytes)
    gen_file(filename,partition + ".img",0)
    last_end_sector = end_sector


def read_xml(filename,search_path):
    rawprogram_xml = ET.parse(filename)
    try:
        xml_iter = rawprogram_xml.iter()
    except AttributeError:
        xml_iter = rawprogram_xml.getiterator()
    for xml_element in xml_iter:
        if xml_element.tag == 'program' and xml_element.attrib['filename'] != '' and care_partition.has_key(xml_element.attrib['label']):
            img_filename = xml_element.attrib['filename']
            img_partiton = xml_element.attrib['label']
            img_start_sector  = xml_element.attrib['start_sector']
            img_number_sector = xml_element.attrib['num_partition_sectors']
	    img_end_sector = (int(img_start_sector) + int(img_number_sector))
            print "Found file:" + img_filename + " partiton:" + img_partiton + " start_sector:" + img_start_sector + " end_sector:%d" % img_end_sector
	    img_filename = find_file(img_filename,search_path)
	    if img_filename is not None:
		    create_img(img_partiton,img_filename,int(img_start_sector),img_end_sector)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(-1)
    try:
	    opts, args = getopt.getopt(sys.argv[1:],"i:?s:o:",["input=","help","search_paths=","out_path="])
    except getopt.GetoptError,err:
	    print str(err)
    OutputFolder = ""
    search_paths = []
    rawprogram_xml_filename = None
    for o, a in opts:
	    if o in ("-i","--input"):
		    rawprogram_xml_filename = a
	    elif o in ("-s","--search_path"):
		    search_paths.append(a)
	    elif o in ("-?","--help"):
		    print "help"
		    sys.exit()
	    elif o in ("-o","--out_path"):
		    OutputFolder = a
    if rawprogram_xml_filename is None:
	    print "Input xml file must specified"
	    sys.exit();
    read_xml(rawprogram_xml_filename,search_paths)
