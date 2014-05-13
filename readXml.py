from xml.etree import ElementTree as ET
import sys

pre=ET.parse(sys.argv[1])
root=pre.getroot()
for child in root.getchildren():
    print child[0].text,
    for elem in child.iter("Phone"):
        print elem.text,
    print 
