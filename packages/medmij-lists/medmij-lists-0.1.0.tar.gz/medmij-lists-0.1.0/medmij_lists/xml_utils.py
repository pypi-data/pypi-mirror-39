""" Util functions for loading XML files
"""
import pkg_resources
from lxml import etree

__all__ = ['xsd_parser_from_resource']


def xsd_parser_from_resource(xsd_resource_name: str) -> etree.XMLParser:
    """ Load a lxml parser with the specified XSD as a schema """
    data = pkg_resources.resource_string(__name__, xsd_resource_name)
    xsdxml = etree.fromstring(data)
    xsd = etree.XMLSchema(xsdxml)
    return etree.XMLParser(schema=xsd)
