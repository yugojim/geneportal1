import pathlib
import json
jsonPath=str(pathlib.Path().absolute()) + "/static/doc/PF21022.json"
print(jsonPath)
Phenopacketjson = json.load(open(jsonPath,encoding="utf-8"))