"""
Defineert de class ZAL
"""
from __future__ import annotations
from typing import AnyStr, Optional, Mapping, Iterator, Tuple
import dataclasses
from lxml import etree

from . import xml_utils

__all__ = ['Gegevensdienst', 'Zorgaanbieder', 'ZAL']


@dataclasses.dataclass(frozen=True)
class Gegevensdienst:
    # pylint: disable=too-few-public-methods
    """
    Een gegevensdienst uit de ZAL zoals beschreven op
    https://afsprakenstelsel.medmij.nl/"""
    id: str
    authorization_endpoint_uri: str
    token_endpoint_uri: str

    def __repr__(self) -> str:
        return f"<Gegevensdienst {self.id!r}>"


@dataclasses.dataclass(frozen=True)
class Zorgaanbieder:
    # pylint: disable=too-few-public-methods
    """
    Een zorgaanbieder uit de ZAL zoals beschreven op
    https://afsprakenstelsel.medmij.nl/"""
    naam: str
    gegevensdiensten: Mapping[str, Gegevensdienst]

    def __repr__(self) -> str:
        return f"<Zorgaanbieder {self.naam!r}>"


class ZAL(Mapping[str, Zorgaanbieder]):
    """
    Een zorgaanbiederslijst zoals beschreven op
    https://afsprakenstelsel.medmij.nl/

    >>> import medmij_lists.tests.testdata
    >>> zal = ZAL(medmij_lists.tests.testdata.ZAL_EXAMPLE_XML)
    >>> za = zal["umcharderwijk@medmij"]
    >>> za
    <Zorgaanbieder 'umcharderwijk@medmij'>
    >>> za.gegevensdiensten["4"]
    <Gegevensdienst '4'>
    """
    NS = "xmlns://afsprakenstelsel.medmij.nl/zorgaanbiederslijst/release2/"
    _parser: Optional[etree.XMLParser] = None
    _zorgaanbieders: Mapping[str, Zorgaanbieder]

    @classmethod
    def _get_xsd_parser(cls) -> etree.XMLParser:
        if cls._parser is None:
            cls._parser = xml_utils.xsd_parser_from_resource("zal.xsd")
        return cls._parser

    def __init__(self, xmldata: AnyStr) -> None:
        parser = self._get_xsd_parser()
        xml = etree.fromstring(xmldata, parser=parser)
        self._zorgaanbieders = self._parse(xml)

    @staticmethod
    def _parse(xml: etree.Element) -> Mapping[str, Zorgaanbieder]:
        nss = {'z': ZAL.NS}

        def gegevensdienst(node: etree.Element) -> Tuple[str, Gegevensdienst]:
            token_endpoint_uri = node.xpath(
                './/z:TokenEndpointuri', namespaces=nss)[0].text
            authorization_endpoint_uri = node.xpath(
                './/z:AuthorizationEndpointuri', namespaces=nss)[0].text
            id_ = node.find('z:GegevensdienstId', namespaces=nss).text
            return id_, Gegevensdienst(
                id=id_,
                token_endpoint_uri=token_endpoint_uri,
                authorization_endpoint_uri=authorization_endpoint_uri,
            )

        def zorgaanbieder(node: etree.Element) -> Tuple[str, Zorgaanbieder]:
            naam = node.find('z:Zorgaanbiedernaam', namespaces=nss).text
            ggs = node.xpath('.//z:Gegevensdienst', namespaces=nss)
            gegevensdiensten = dict(gegevensdienst(node) for node in ggs)
            return naam, Zorgaanbieder(naam=naam,
                                       gegevensdiensten=gegevensdiensten)

        xpath = xml.xpath(f'//z:Zorgaanbieder', namespaces=nss)
        return dict(zorgaanbieder(node) for node in xpath)

    def __getitem__(self, key: str) -> Zorgaanbieder:
        return self._zorgaanbieders[key]

    def __iter__(self) -> Iterator:
        return self._zorgaanbieders.__iter__()

    def __len__(self) -> int:
        return self._zorgaanbieders.__len__()
