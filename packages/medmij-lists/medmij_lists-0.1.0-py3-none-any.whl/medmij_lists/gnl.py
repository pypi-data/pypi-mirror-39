"""
Defineert de class GNL
"""
from __future__ import annotations
from typing import AnyStr, Optional, Mapping, Iterator, Tuple
import dataclasses
from lxml import etree

from . import xml_utils

__all__ = ['GNL']


@dataclasses.dataclass(frozen=True)
class Gegevensdienst:
    # pylint: disable=too-few-public-methods
    """
    Een gegevensdienst zoals beschreven op
    https://afsprakenstelsel.medmij.nl/"""
    id: str
    weergavenaam: str

    def __repr__(self) -> str:
        return f"<Gegevensdienst {self.id!r}>"


class GNL(Mapping[str, Gegevensdienst]):
    """
    Een zorgaanbiederslijst zoals beschreven op
    https://afsprakenstelsel.medmij.nl/
    """
    NS = "xmlns://afsprakenstelsel.medmij.nl/gegevensdienstnamenlijst/release1/"
    _parser: Optional[etree.XMLParser] = None
    _gegevensdiensten: Mapping[str, Gegevensdienst]

    @classmethod
    def _get_xsd_parser(cls) -> etree.XMLParser:
        if cls._parser is None:
            cls._parser = xml_utils.xsd_parser_from_resource("gnl.xsd")
        return cls._parser

    def __init__(self, xmldata: AnyStr) -> None:
        parser = self._get_xsd_parser()
        xml = etree.fromstring(xmldata, parser=parser)
        self._gegevensdiensten = self._parse(xml)

    @staticmethod
    def _parse(xml: etree.Element) -> Mapping[str, Gegevensdienst]:
        nss = {'g': GNL.NS}

        def gegevensdienst(node: etree.Element) -> Tuple[str, Gegevensdienst]:
            id_ = node.find('g:GegevensdienstId', namespaces=nss).text
            display_name = node.find('g:Weergavenaam', namespaces=nss).text

            return id_, Gegevensdienst(
                id=id_,
                weergavenaam=display_name,
            )

        gegevensdiensten = xml.xpath(f'//g:Gegevensdiensten', namespaces=nss)[0]

        return dict(gegevensdienst(gd) for gd in gegevensdiensten)

    def __getitem__(self, key: str) -> Gegevensdienst:
        return self._gegevensdiensten[key]

    def __iter__(self) -> Iterator:
        return self._gegevensdiensten.__iter__()

    def __len__(self) -> int:
        return self._gegevensdiensten.__len__()
