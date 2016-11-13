#!/usr/bin/env python3
from invoke import task
import os
import json
from .import_HC_data import import_HC_data, export_strain_select_json,\
    export_strain_node_lists, export_protein_data

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
SalmoNetJson = "SalmoNet.json"
temp_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir, "scripts","temp_data"))
data_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir, "data"))
dev_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir, "template","src","data"))
deploy_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir,"SalmoNet","static","data"))
download_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir,"SalmoNet","static","download"))
pages_path = os.path.abspath(os.path.join(ROOT_PATH, os.pardir,"SalmoNet","content","protein"))

@task()
def test(ctx):
    ctx.run("echo \"data - OK\"")

@task()
def clear_dev(ctx):
    ctx.run("rm -rf %s/*" % dev_path, warn=True)

@task()
def clear_deploy(ctx):
    ctx.run("rm -rf %s/*" % deploy_path, warn=True)
    ctx.run("rm -rf %s/*" % download_path, warn=True)

@task()
def clear_protein_pages(ctx):
    ctx.run("rm -rf %s/*" % pages_path, warn=True)

@task()
def clear_temp(ctx):
    ctx.run("rm -rf %s/*" % temp_path)

@task(clear_temp)
def make_dirs(ctx):
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    if not os.path.exists(pages_path):
        os.makedirs(pages_path)
    if not os.path.exists(download_path):
        os.makedirs(download_path)

@task(make_dirs)
def import_data(ctx):
    SalmoNet = import_HC_data(os.path.join(data_path, "HC_nodes.csv"), os.path.join(data_path,"HC_interactions.csv"))
    with open(os.path.join(temp_path, SalmoNetJson), "w") as f:
        json.dump(SalmoNet, f)

@task(import_data)
def export_strain_select(ctx):
    with open(os.path.join(temp_path, SalmoNetJson)) as data_file:
        SalmoNet = json.load(data_file)
        export_strain_select_json(SalmoNet, os.path.join(temp_path, "strain_select.json"))

@task(import_data)
def export_strain_nodes(ctx):
    with open(os.path.join(temp_path, SalmoNetJson)) as data_file:
        SalmoNet = json.load(data_file)
        export_strain_node_lists(SalmoNet, temp_path)

@task(export_strain_select, export_strain_nodes, clear_dev)
def copy_dev(ctx):
    ctx.run("cp %s/strain_select.json %s/" % (temp_path, dev_path))
    ctx.run("cp %s/nodes* %s/" % (temp_path, dev_path))

@task(export_strain_select, export_strain_nodes, clear_deploy)
def copy_deploy(ctx):
    ctx.run("cp %s/strain_select.json %s/" % (temp_path, deploy_path))
    ctx.run("cp %s/nodes* %s/" % (temp_path, deploy_path))
    ctx.run("cp %s/* %s/" % (os.path.join(data_path, "download"), download_path))

@task(clear_protein_pages, import_data)
def export_protein_pages(ctx, just_one=False):
    with open(os.path.join(temp_path, SalmoNetJson)) as data_file:
        SalmoNet = json.load(data_file)
        export_protein_data(SalmoNet, pages_path, just_one)
