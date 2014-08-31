#!/usr/bin/env python

import sys
import xml.dom.minidom

(fileName, attrName) = sys.argv[1:]

xmldoc = xml.dom.minidom.parse( fileName )
print xmldoc.childNodes[0].getAttribute( attrName )

