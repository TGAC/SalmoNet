#!/usr/bin/env python3
from invoke import task
import os
import json
from .import_HC_data import import_HC_data, export_strain_select_json,\
    export_strain_node_lists, export_protein_data

SalmoNetJson = "scripts/temp_data/SalmoNet.json"
temp_path = "scripts/temp_data"
dev_path = "template/src/data"
deploy_path = "SalmoNet/static/data"
pages_path = "SalmoNet/content/protein"

@task()
def test(ctx):
    ctx.run("echo \"data - OK\"")

@task()
def clear_dev(ctx):
    ctx.run("rm -rf %s/*" % dev_path, warn=True)

@task()
def clear_deploy(ctx):
    ctx.run("rm -rf %s/*" % deploy_path, warn=True)
    ctx.run("rm -rf SalmoNet/static/download/*", warn=True)

@task()
def clear_protein_pages(ctx):
    ctx.run("rm -rf %s/*" % pages_path, warn=True)

@task()
def clear_temp(ctx):
    ctx.run("rm -rf %s/*" % temp_path)

@task(clear_temp)
def import_data(ctx):
    SalmoNet = import_HC_data("data/HC_nodes.csv", "data/HC_interactions.csv")
    with open(SalmoNetJson, "w") as f:
        json.dump(SalmoNet, f)

@task(import_data)
def export_strain_select(ctx):
    with open(SalmoNetJson) as data_file:
        SalmoNet = json.load(data_file)
        export_strain_select_json(SalmoNet, "scripts/temp_data/strain_select.json")

@task(import_data)
def export_strain_nodes(ctx):
    with open(SalmoNetJson) as data_file:
        SalmoNet = json.load(data_file)
        export_strain_node_lists(SalmoNet, "scripts/temp_data")

@task(export_strain_select, export_strain_nodes, clear_dev)
def copy_dev(ctx):
    ctx.run("cp %s/strain_select.json %s/" % (temp_path, dev_path))
    ctx.run("cp %s/nodes* %s/" % (temp_path, dev_path))

@task(export_strain_select, export_strain_nodes, clear_deploy)
def copy_deploy(ctx):
    ctx.run("cp %s/strain_select.json %s/" % (temp_path, deploy_path))
    ctx.run("cp %s/nodes* %s/" % (temp_path, deploy_path))
    ctx.run("cp data/download/* SalmoNet/static/download/")

@task(clear_protein_pages, import_data)
def export_protein_pages(ctx, just_one=False):
    with open(SalmoNetJson) as data_file:
        SalmoNet = json.load(data_file)
        export_protein_data(SalmoNet, pages_path, just_one)
