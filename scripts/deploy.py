#!/usr/bin/env python3
import subprocess
import os
import json
from import_HC_data import import_HC_data, export_strain_select_json,\
    export_strain_node_lists, export_protein_data

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
SalmoNetJson = "SalmoNet.json"
temp_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir, "scripts","temp_data"))
data_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir, "data"))
dev_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir, "template","src","data"))
deploy_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir,"SalmoNet","static","data"))
download_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir,"SalmoNet","static","download"))
pages_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir,"SalmoNet","content","protein"))

# make dirs
if not os.path.exists(temp_path):
    os.makedirs(temp_path)
if not os.path.exists(pages_path):
    os.makedirs(pages_path)
if not os.path.exists(download_path):
    os.makedirs(download_path)
if not os.path.exists(dev_path):
    os.makedirs(dev_path)

# clear temp
subprocess.call("rm -rf %s/*" % temp_path, stdout=subprocess.PIPE)

# import data
SalmoNet = import_HC_data(os.path.join(data_path, "HC_nodes.csv"), os.path.join(data_path,"HC_interactions.csv"))
with open(os.path.join(temp_path, SalmoNetJson), "w") as f:
    json.dump(SalmoNet, f)

# export strain nodes
with open(os.path.join(temp_path, SalmoNetJson)) as data_file:
    SalmoNet = json.load(data_file)
    export_strain_node_lists(SalmoNet, temp_path)

# export strain select
with open(os.path.join(temp_path, SalmoNetJson)) as data_file:
    SalmoNet = json.load(data_file)
    export_strain_select_json(SalmoNet, os.path.join(temp_path, "strain_select.json"))

# clear protein pages
subprocess.call("rm -rf %s/*" % pages_path, stdout=subprocess.PIPE)

# export protein pages
with open(os.path.join(temp_path, SalmoNetJson)) as data_file:
    SalmoNet = json.load(data_file)
    export_protein_data(SalmoNet, pages_path, just_one)

# copy deploy
subprocess.call("cp %s %s" % (os.path.join(temp_path, "strain_select.json"), os.path.join(deploy_path, "strain_select.json")), stdout=subprocess.PIPE)
subprocess.call("for file in %s*; do cp \"$file\" \"%s/$file\";done"  % (os.path.join(temp_path,"nodes"), deploy_path), stdout=subprocess.PIPE)
subprocess.call("cp %s %s" % (os.path.join(data_path, "download"), download_path), stdout=subprocess.PIPE)
