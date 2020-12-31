# KIT Modulhandbuch-Extractor

Dieses inoffizielle Projekt extrahiert sämtliche Module und Teilleistungen eines [KIT](https://kit.edu) Studiengangs und speichert sie in einer JSON oder ggf. CSV Datei ab.

Module und Teilleistungen von der Webseite scrapen:
```python extractor.py <Studiengang>```

Erstellte JSON aus dem extractor in CSV Dateien convertierten:
```python csv_creator.py <Studiengang>```

Unterstützte Studiengänge können in der [constants.py](constants.py) eingesehen werden.
