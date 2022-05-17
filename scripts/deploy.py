#!/usr/bin/env python3
import subprocess
import os
import sys
import json
import shutil
from import_HC_data import import_HC_data, export_strain_select_json,\
    export_strain_node_lists, export_protein_data

DEV = False
if len(sys.argv) == 2:
    if sys.argv[1] == "dev":
        DEV = True

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
SalmoNetJson = "SalmoNet.json"
temp_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir, "scripts","temp_data"))
data_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir, "data"))
dev_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir, "template","src","data"))
deploy_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir,"SalmoNet","static","data"))
download_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir,"SalmoNet","static","download"))
pages_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir,"SalmoNet","content","protein"))

strains_long_name = {
    "SALA4": "Salmonella agona (strain SL483)",
    "SALAR": "Salmonella arizonae (strain ATCC BAA-731 / CDC346-86 / RSK2980)",
    "SALBC": "Salmonella bongori (strain ATCC 43975 / DSM 13772 / NCTC 12419)",
    "SALCH": "Salmonella choleraesuis (strain SC-B67)",
    "SALDC": "Salmonella dublin (strain CT_02021853)",
    "SALEP": "Salmonella enteritidis PT4 (strain P125109)",
    "SALG2": "Salmonella gallinarum (strain 287/91 / NCTC 13346)",
    "SALHS": "Salmonella heidelberg (strain SL476)",
    "SALNS": "Salmonella newport (strain SL254)",
    "SALPK": "Salmonella paratyphi A (strain AKU_12601)",
    "SALPA": "Salmonella paratyphi A (strain ATCC 9150 / SARB42)",
    "SALPB": "Salmonella paratyphi B (strain ATCC BAA-1250 / SPB7)",
    "SALPC": "Salmonella paratyphi C (strain RKS4594)",
    "SALSV": "Salmonella schwarzengrund (strain CVM19633)",
    "SALTI": "Salmonella typhi",
    "SALT1": "Salmonella typhimurium (strain 14028s / SGSC 2262)",
    "SALT4": "Salmonella typhimurium (strain 4/74)",
    "SALTD": "Salmonella typhimurium (strain D23580)",
    "SALTY": "Salmonella typhimurium (strain LT2 / SGSC1412 / ATCC 700720)",
    "SALTS": "Salmonella typhimurium (strain SL1344)",
}

# make dirs
print("make dirs")
if not os.path.exists(temp_path):
    os.makedirs(temp_path)
if not os.path.exists(pages_path):
    os.makedirs(pages_path)
if not os.path.exists(download_path):
    os.makedirs(download_path)
if not os.path.exists(dev_path):
    os.makedirs(dev_path)
if not os.path.exists(deploy_path):
	os.makedirs(deploy_path)

# clear temp
print("clear temp")
subprocess.call(["rm", "-rf", temp_path+"/*"], stdout=subprocess.PIPE)

# import data
print("import data")
SalmoNet = import_HC_data(
    os.path.join(data_path, "HC_nodes_2022_05_17.csv"),
    os.path.join(data_path, "HC_interactions_2022_05_16.csv"),
    os.path.join(data_path, "HC_xref_source_new.csv"),
    os.path.join(data_path, "HC_xref_matrix_new.csv"),
    os.path.join(data_path, "HC_xref_new.csv"),
)
with open(os.path.join(temp_path, SalmoNetJson), "w") as f:
    json.dump(SalmoNet, f)

# export strain nodes
print("export strain nodes")
with open(os.path.join(temp_path, SalmoNetJson)) as data_file:
    SalmoNet = json.load(data_file)
    export_strain_node_lists(SalmoNet, temp_path)

# export strain select
print("export strain select")
with open(os.path.join(temp_path, SalmoNetJson)) as data_file:
    SalmoNet = json.load(data_file)
    export_strain_select_json(SalmoNet, os.path.join(temp_path, "strain_select.json"), strains_long_name)

# clear protein pages
print("clear protein pages")
subprocess.call(["rm","-rf", pages_path+"/*"], stdout=subprocess.PIPE)

# export protein pages
print("export protein pages")
with open(os.path.join(temp_path, SalmoNetJson)) as data_file:
    SalmoNet = json.load(data_file)
    export_protein_data(SalmoNet, pages_path, DEV)

# copy deploy
print("copy deploy")
for src_file in os.listdir(temp_path):
	if src_file == "SalmoNet.json":
		continue
	shutil.copy(os.path.join(temp_path, src_file), os.path.join(deploy_path,src_file))
for src_file in os.listdir(os.path.join(data_path, "download")):
	shutil.copy(os.path.join(data_path, "download", src_file), os.path.join(download_path,src_file))
