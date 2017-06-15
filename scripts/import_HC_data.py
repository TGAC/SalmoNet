#!/bin/env python3

import csv
import json
import yaml

def import_HC_data(node_file, interaction_file):
    SalmoNet = {"node": {}, "interaction": {}, "groups": {}, "strains": []}
    with open(node_file) as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)
        for row in reader:
            SalmoNet["node"][row[0]] = {
                "name": row[1],
                "locus": row[2].replace(",", ";"),
                "group": row[3],
                "strain": row[4],
                "num_ortholog": 0,
                "num_interaction": 0,
                "interactions": [],
            }
            if row[3] not in SalmoNet["groups"]:
                SalmoNet["groups"][row[3]] = []
            add_group = {"stain": row[4], "uniprot": row[0]}
            if add_group not in SalmoNet["groups"][row[3]]:
                SalmoNet["groups"][row[3]].append(add_group)
            if row[4] not in SalmoNet["strains"]:
                SalmoNet["strains"].append(row[4])
    with open(interaction_file) as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)
        for row in reader:
            ref = row[2].replace(",", "").replace("__", "_").split("_")
            SalmoNet["interaction"]["%s-%s"%(row[0],row[1])] = {
                "source": row[0],
                "target": row[1],
                "ref": ref,
                "layer": row[3],
            }
            SalmoNet["node"][row[0]]["num_interaction"] += 1
            SalmoNet["node"][row[1]]["num_interaction"] += 1
            icsv = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
                SalmoNet["node"][row[0]]["name"],
                SalmoNet["node"][row[1]]["name"],
                " ".join(ref),
                row[3],
                SalmoNet["node"][row[0]]["locus"],
                SalmoNet["node"][row[1]]["locus"],
                row[0],
                row[1],
                SalmoNet["node"][row[0]]["group"],
                SalmoNet["node"][row[1]]["group"]
                )
            SalmoNet["node"][row[0]]["interactions"].append(icsv)
            SalmoNet["node"][row[1]]["interactions"].append(icsv)
    for node in SalmoNet["node"]:
        SalmoNet["node"][node]["num_ortholog"] = len(SalmoNet["groups"][SalmoNet["node"][node]["group"]])
        SalmoNet["node"][node]["orthologs"] = SalmoNet["groups"][SalmoNet["node"][node]["group"]]
    return SalmoNet


def export_strain_select_json(SalmoNet, out_file):
    select = []
    select.append({"value": "Select a strain", "id": 0})
    for id, strain in enumerate(SalmoNet["strains"]):
        select.append({"id": id+1, "value": strain})
    with open(out_file, "w") as f:
        json.dump(select, f)


def export_strain_node_lists(SalmoNet, files_prefix):
    for id, strain in enumerate(SalmoNet["strains"]):
        with open("%s/nodes%s.csv" % (files_prefix, id+1), "w") as f:
            for nid, node in enumerate(SalmoNet["node"]):
                if SalmoNet["node"][node]["strain"] == strain:
                    f.write("%s,%s,%s,%s,%s,%s\n" % (
                        nid,
                        node,
                        SalmoNet["node"][node]["name"],
                        SalmoNet["node"][node]["locus"],
                        SalmoNet["node"][node]["num_ortholog"],
                        SalmoNet["node"][node]["num_interaction"],
                    ))

def export_protein_data(SalmoNet, path, just_one=False):
    for uniprot in SalmoNet["node"]:
        if just_one:
            #uniprot = "E1WFQ7"
            uniprot = "B5R5K2"
        with open("%s/%s.md" % (path, uniprot), "w") as f:
            md_data = {}
            md_data["title"] = uniprot
            md_data["description"] = uniprot
            md_data["date"] = "2016-07-01"
            #
            md_data["genename"] = SalmoNet["node"][uniprot]["name"]
            md_data["locus"] = SalmoNet["node"][uniprot]["locus"]
            md_data["strain"] = SalmoNet["node"][uniprot]["strain"]
            md_data["orthologs"] = SalmoNet["node"][uniprot]["orthologs"]
            md_data["uniprot"] = uniprot
            md_data["interactioncsv"] = "\n".join(SalmoNet["node"][uniprot]["interactions"])
            #
            md = yaml.dump(md_data, allow_unicode=True,
                      default_flow_style=False,
                      explicit_start=True, explicit_end=True,
                      default_style="'", line_break="/n")[:-4]
            md += "---\n"
            f.write(md)
        if just_one:
            return
