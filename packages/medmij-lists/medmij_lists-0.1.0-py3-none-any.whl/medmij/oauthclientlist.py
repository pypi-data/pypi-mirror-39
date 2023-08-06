"""
Defineert de class OAuthclientList
"""
# from __future__ import annotations
from typing import AnyStr, Optional, Mapping, Iterator, Tuple
import dataclasses
from lxml import etree

from . import xml_utils

__all__ = ['OAuthclient', 'OAuthclientList']


@dataclasses.dataclass(frozen=True)
class OAuthclient:
    # pylint: disable=too-few-public-methods
    """
    Een OAuth CLient uit de OAuth Client List zoals beschreven op
    https://afsprakenstelsel.medmij.nl/"""
    hostname: str
    organisatienaam: str


class OAuthclientList(Mapping[str, OAuthclient]):
    """
    Een OAuth Client List zoals beschreven op
    https://afsprakenstelsel.medmij.nl/

    >>> import medmij.tests.testdata
    >>> ocl = OAuthclientList(
    ...           medmij.tests.testdata.OAUTHCLIENTLIST_EXAMPLE_XML)
    >>> len(ocl)
    2
    >>> for hostname in ocl:
    ...     print(f"{hostname}->{ocl[hostname].organisatienaam}")
    medmij.deenigeechtepgo.nl->De Enige Echte PGO
    pgocluster68.personalhealthprovider.net->Unstealth Health Midden-Nederland

    OAuthclientList valideert de xml met een XSD:

    >>> OAuthclientList('<test></test>')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    lxml.etree.XMLSyntaxError: Element 'test': No matching global declaration \
available for the validation root.
    """
    NS = "xmlns://afsprakenstelsel.medmij.nl/oauthclientlist/release2/"
    _parser: Optional[etree.XMLParser] = None
    _oauthclients: Mapping[str, OAuthclient]

    @classmethod
    def _get_xsd_parser(cls) -> etree.XMLParser:
        if cls._parser is None:
            cls._parser = xml_utils.xsd_parser_from_resource(
                "oauthclientlist.xsd")
        return cls._parser

    def __init__(self, xmldata: AnyStr) -> None:
        parser = self._get_xsd_parser()
        xml = etree.fromstring(xmldata, parser=parser)
        self._oauthclients = self._parse(xml)

    @staticmethod
    def _parse(xml: etree.Element) -> Mapping[str, OAuthclient]:
        nss = {'o': OAuthclientList.NS}

        def oauthclient(node: etree.Element) -> Tuple[str, OAuthclient]:
            hostname = node.find('o:Hostname', namespaces=nss).text
            organisatienaam = node.find(
                'o:OAuthclientOrganisatienaam', namespaces=nss).text
            return hostname, OAuthclient(hostname=hostname,
                                         organisatienaam=organisatienaam)

        xpath = xml.xpath(f'//o:OAuthclient', namespaces=nss)
        return dict(oauthclient(node) for node in xpath)

    def __getitem__(self, key: str) -> OAuthclient:
        return self._oauthclients[key]

    def __iter__(self) -> Iterator:
        return self._oauthclients.__iter__()

    def __len__(self) -> int:
        return self._oauthclients.__len__()
