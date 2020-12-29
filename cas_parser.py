from typing import List, Tuple
import requests
import xml.etree.ElementTree as ET

from constants import *

ns = {"": "http://www.w3.org/1999/xhtml"}
ET.register_namespace("", "http://www.w3.org/1999/xhtml")


def _strip_text(text: str) -> str:
    return text.strip().replace("\xa0", " ").replace("\xa098", " ")


def _xml_from_url(url: str) -> ET.Element:
    return ET.fromstring(requests.get(url).content)


def _inner_xml(element: ET.Element) -> str:
    return (element.text or "") + "".join(
        ET.tostring(e, "unicode").replace(' xmlns="http://www.w3.org/1999/xhtml"', "")
        for e in element
    )


################################################################
# PARSE LIST
################################################################


def _parse_xml_columns(table: ET.Element) -> List[str]:
    tds = table.find("tbody/tr", ns).findall("th", ns)
    return [_strip_text(x.text) for x in tds]


def _parse_xml_row(columns: List[str], tds: ET.Element) -> dict:
    assert len(columns) == len(tds)

    result = {}
    for column, td in zip(columns, tds):
        a_tag = td.find("a", ns)
        text: str
        if a_tag is not None:
            text = a_tag.text
            result["href"] = a_tag.attrib["href"]
        else:
            text = td.text

        text = _strip_text(text)
        result[column] = text
    return result


def _parse_xml_list(root: ET.Element) -> List[dict]:
    result = []

    table = root.find("body/form/div/div/div/table", ns)
    columns = _parse_xml_columns(table)
    tbody = table.findall("tbody", ns)[1]
    for elem in tbody.findall("tr", ns):
        cl = elem.attrib["class"]
        if cl == "odd" or cl == "even":
            tds = elem.findall("td", ns)
            result.append(_parse_xml_row(columns, tds))
    return result


################################################################
# PARSE ADDITIONAL INFO
################################################################


def _parse_xml_info(root: ET.Element) -> dict:
    result = {}
    detailNode = root.find('.//div[@id="tab-container-details"]', ns)
    if detailNode is None:
        detailNode = root.find('.//div[@id="tab-container-detail"]', ns)
    infos = detailNode.findall('.//div[@class="field"]', ns)
    for info in infos:
        key, value = info.findall("div", ns)
        result[_strip_text(key.text)[:-1]] = _strip_text(_inner_xml(value))

    return result


################################################################
# API METHODS
################################################################


def get_modules(index_url: str) -> List[dict]:
    root = _xml_from_url(index_url)
    return _parse_xml_list(root)


def parse_module(module_url: str) -> Tuple[List[dict], dict]:
    root = _xml_from_url(module_url)
    courses = _parse_xml_list(root)
    additional_info = _parse_xml_info(root)
    return courses, additional_info


def parse_course(course_url: str) -> dict:
    root = _xml_from_url(course_url)
    additional_info = _parse_xml_info(root)
    return additional_info
