"""
Defineert de class Whitelist
"""
from __future__ import annotations
from typing import AnyStr, Set, Optional
from lxml import etree

from . import xml_utils


class Whitelist(Set[str]):
    """
    Een whitelist zoals beschreven op https://afsprakenstelsel.medmij.nl/


    >>> import medmij_lists.tests.testdata
    >>> w = Whitelist(medmij_lists.tests.testdata.WHITELIST_EXAMPLE_XML)
    >>> "rcf-rso.nl" in w
    True
    >>> "taart" in w
    False
    """
    NS = "xmlns://afsprakenstelsel.medmij.nl/whitelist/release2/"
    _parser: Optional[etree.XMLParser] = None

    @classmethod
    def _get_xsd_parser(cls) -> etree.XMLParser:
        if cls._parser is None:
            cls._parser = xml_utils.xsd_parser_from_resource('whitelist.xsd')

        return cls._parser

    def __init__(self, xmldata: AnyStr) -> None:
        parser = self._get_xsd_parser()
        xml = etree.fromstring(xmldata, parser=parser)
        self._hostnames = self._parse(xml)

    def __contains__(self, key: object) -> bool:
        return key in self._hostnames

    @staticmethod
    def _parse(xml: etree.Element) -> Set[str]:
        nss = {'w': Whitelist.NS}
        nodes = xml.xpath(f'//w:MedMijNodes', namespaces=nss)[0]

        def hostname(node: etree.Element) -> str:
            return node.find('w:Hostname', namespaces=nss).text

        return set(hostname(node) for node in nodes)

    def __iter__(self):
        return self._hostnames.__iter__()

    def __len__(self):
        return self._hostnames.__len__()
