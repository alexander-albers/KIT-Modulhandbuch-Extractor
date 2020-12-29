import csv
import xml.etree.ElementTree as ET
import requests
from time import sleep
from tqdm import tqdm

root = ET.parse("tree.xml").getroot()
namespace = {"html": "http://www.w3.org/1999/xhtml"}
table = root.find("html:body/html:form/html:div/html:div/html:div/html:table", namespace)
tbody = table.findall("html:tbody", namespace)[1]

base_url = "https://campus.kit.edu/sp/campus/all/"

with open("sub_tree.csv", "w") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["Modul", "Kennung", "Titel", "Version", "LP", "Semester"])
    for elem in tqdm(tbody.findall("html:tr", namespace)):
        cl = elem.attrib["class"]
        if cl == "odd" or cl == "even":
            td = elem.find("html:td", namespace)
            id = td.find("html:a", namespace).text
            url = td.find("html:a", namespace).attrib["href"]

            event_root = ET.fromstring(requests.get(base_url + url).content)
            event_table = event_root.find("html:body/html:form/html:div/html:div/html:div/html:table", namespace)
            event_tbody = event_table.findall("html:tbody", namespace)[1]

            for event_elem in event_tbody.findall("html:tr", namespace):
                event_cl = event_elem.attrib["class"]
                if event_cl == "odd" or event_cl == "even":
                    tds = event_elem.findall("html:td", namespace)
                    event_id, name = [x.find("html:a", namespace).text for x in tds[:2]]
                    version, _, lp, sem = [x.text for x in tds[2:]]
                    writer.writerow([id, event_id, name.replace("\n", ""), version, lp, sem])

            sleep(1)

