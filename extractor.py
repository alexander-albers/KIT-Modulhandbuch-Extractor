import cas_parser
from constants import *
from time import sleep
import json
from tqdm import tqdm
import sys


degree = sys.argv[1] if len(sys.argv) > 1 else INDEX_URLS[0]

################################################################
# GET MODULES
################################################################

subjects = cas_parser.get_modules(INDEX_URLS[degree])
for subject in tqdm(subjects, "Suche Module"):
    modules = cas_parser.get_modules(BASE_URL + subject["href"])
    sleep(1)
    subject["Module"] = modules

modules = [module for subject in subjects if "Module" in subject for module in subject["Module"]]
unique_module_ids = set((module["Kennung"] for module in modules))
print(f"{len(modules)} Module gefunden (davon {len(unique_module_ids)} eindeutig)")


################################################################
# GET COURSES
################################################################

for module_id in tqdm(unique_module_ids, "Suche Veranstaltungen"):
    module_url = next((module for module in modules if module["Kennung"] == module_id))["href"]
    courses, module_info = cas_parser.parse_module(BASE_URL + module_url)
    for module in (module for module in modules if module["Kennung"] == module_id):
        module.update(module_info)
        module["Veranstaltungen"] = courses
    sleep(1)

courses = [course for module in modules if "Veranstaltungen" in module for course in module["Veranstaltungen"]]
unique_course_ids = set((course["Kennung"] for course in courses))
print(f"{len(courses)} Veranstaltungen gefunden (davon {len(unique_course_ids)} eindeutig)")


################################################################
# PARSE COURSE INFO
################################################################

for course_id in tqdm(unique_course_ids, "Lade Veranstaltungen"):
    course_url = next((course for course in courses if course["Kennung"] == course_id))["href"]
    course_info = cas_parser.parse_course(BASE_URL + course_url)
    for course in (course for course in courses if course["Kennung"] == course_id):
        course.update(course_info)
    sleep(1)


################################################################
# EXPORT
################################################################

print("Exportiere...", end="")
with open(f"data/Modulhandbuch-{degree}.json", "w") as f:
    json.dump(subjects, f)
print("fertig!")
