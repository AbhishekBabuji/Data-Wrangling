#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "velachery_chennai.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Extension", "Road", "Street", "Avenue"]

mapping = { "St": "Street",
			"st": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd": "Road",
            "Rd.": "Road",
            "Extn": "Extension",
            "Extn.": "Extension",
            "Strret": "Street",
            "strret": "Street"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    pprint.pprint(dict(street_types))
    return street_types
#    
    

def update_name(name, mapping):
    name_array = name.split(' ')
    last = name_array[-1]
    if last in mapping.keys():
    	name_array[-1] = mapping[last]
    return ' '.join(name_array)

# Audit Postal Code

def audit_postal_code(error_codes, postal_codes, this_postal_code):
    # Append incorrect zip codes to list
    if this_postal_code.isdigit() == False:
        error_codes.append(this_postal_code)
    elif len(this_postal_code) != 6:
        error_codes.append(this_postal_code)
    else:
        postal_codes.update([this_postal_code])

def is_postal_code(elem):
    # Identify element tag as postal code
    return (elem.attrib['k'] == "addr:postcode")
    
def audit_post(osmfile):
    # Parse osm file for incorrect postal codes
    osm_file = open(osmfile, "r")
    error_codes = []
    postal_codes = set([])
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postal_code(tag):
                    audit_postal_code(error_codes, postal_codes, tag.attrib["v"]) 
    return error_codes, postal_codes

bad_list, good_list = audit_post(OSMFILE)


print(bad_list)


def test():
    st_types = audit(OSMFILE)
    
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)      
    	print(better_name)		
            
if __name__ == '__main__':
	test()