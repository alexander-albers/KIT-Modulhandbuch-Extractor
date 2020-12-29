import json
from typing import List
import pandas as pd
import sys
from constants import *


degree = sys.argv[1] if len(sys.argv) > 1 else INDEX_URLS[0]

with open(f"data/Modulhandbuch-{degree}.json") as f:
    root = json.load(f)


def create_unique(mylist: List[dict], key: str = "Kennung") -> list:
    seen = set()
    return [seen.add(obj[key]) or obj for obj in mylist if obj[key] not in seen]


modules = create_unique(
    [module for subject in root if "Module" in subject for module in subject["Module"]]
)
modules = modules
courses = []
for module in modules:
    for course in module["Veranstaltungen"]:
        course["Modul"] = module["Kennung"]
        courses.append(course)


module_df = pd.DataFrame.from_dict(modules)
module_df = module_df[
    ["Kennung", "Titel", "Ver", "Gew", "LP", "Sem", "Modulturnus", "Moduldauer"]
]
module_df = module_df.replace("\n", "", regex=True)
module_df.to_csv(f"data/Module-{degree}.csv", index=False, sep=";")


course_df = pd.DataFrame.from_dict(courses)
course_df = course_df[["Modul", "Kennung", "Titel", "Ver", "Gew", "LP", "Sem"]]
course_df = course_df.replace("\n", "", regex=True)
course_df.to_csv(f"data/Veranstaltungen-{degree}.csv", index=False, sep=";")
