#!/bin/env python3

import csv
import json
import yaml

def import_HC_data(node_file, interaction_file, xref_source_file, xref_matrix_file, xref_i_file):
    SalmoNet = {"node": {}, "interaction": {}, "groups": {}, "strains": []}
    #lode xrefs
    xref = {"source": {}, "matrix": {}}
    with open(xref_source_file) as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            xref["source"][row[0]] = row[2].split(",")
    with open(xref_matrix_file) as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            for m in row[0].split(","):
                xref["matrix"][m] = row[1].split(",")
    with open(xref_i_file) as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            xref["matrix"][";".join(row[0:2])] = row[4].split(",")
    #load node data
    with open(node_file) as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)
        for row in reader:
            SalmoNet["node"][row[0]] = {
                "name": row[1],
                "locus": row[2].replace(",", ";"),
                "old_locus": row[3].replace(",", ";"),
                "group": row[4],
                "strain": row[5],
                "num_ortholog": 0,
                "num_interaction": 0,
                "interactions": [],
                "networkjson": [],
            }
            if row[4] not in SalmoNet["groups"]:
                SalmoNet["groups"][row[4]] = []
            add_group = {"stain": row[5], "uniprot": row[0]}
            if add_group not in SalmoNet["groups"][row[4]]:
                SalmoNet["groups"][row[4]].append(add_group)
            if row[5] not in SalmoNet["strains"]:
                SalmoNet["strains"].append(row[5])
    #load interactions
    with open(interaction_file) as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)
        for row in reader:

            if row[0] == "NULL" or row[1] == "NULL":
                continue

            ref = row[2].replace(",", "").replace("__", "_").split("_")
            pmids = []
            for s in xref["source"][row[2]]:
                if s == "matrix":
                    if SalmoNet["node"][row[0]]["group"] not in xref["matrix"]:
                        xref_based_on_orthology_matrix = "based on orthology"
                    pmids.append(xref_based_on_orthology_matrix)
                elif s == "exp":
                    if ";".join(row[0:2]) not in xref["matrix"]:
                        xref_based_on_orthology_exp = "based on orthology"
                    pmids.append(xref_based_on_orthology_exp)
                else:
                    pmids.append(s)

            pmlink = "https://www.ncbi.nlm.nih.gov/pubmed/?term=" + "+OR+".join([p+"%5Buid%5D" for p in pmids])
            pmlink = "<a href=\""+pmlink+"\" target=\"_blank\"><i class=\"uk-icon-newspaper-o\"></i></a>"
            if "based on orthology" in pmlink:
                pmlink = "<a href='#legendmodal'><i class='uk-icon-newspaper-o'></i></a>"
                print(ref)
            
            SalmoNet["interaction"]["%s-%s"%(row[0],row[1])] = {
                "source": row[0],
                "target": row[1],
                "ref": ref,
                "layer": row[3],
                "pmids": ",".join(pmids),
                "pmlink": pmlink,
            }
            
            SalmoNet["node"][row[0]]["num_interaction"] += 1
            if SalmoNet["node"][row[0]] != SalmoNet["node"][row[1]]:
                SalmoNet["node"][row[1]]["num_interaction"] += 1
            icsv = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
                SalmoNet["node"][row[0]]["name"],
                SalmoNet["node"][row[1]]["name"],
                " ".join(ref)+"&ensp;"+pmlink,
                row[3],
                SalmoNet["node"][row[0]]["locus"],
                SalmoNet["node"][row[1]]["locus"],
                row[0],
                row[1],
                SalmoNet["node"][row[0]]["group"],
                SalmoNet["node"][row[1]]["group"],
                "\"%s\""%SalmoNet["node"][row[0]]["strain"],
                "\"%s\""%SalmoNet["node"][row[1]]["strain"],
                " ".join(ref),
                ",".join(pmids),
                )
            SalmoNet["node"][row[0]]["interactions"].append(icsv)
            if SalmoNet["node"][row[0]] != SalmoNet["node"][row[1]]:
                SalmoNet["node"][row[1]]["interactions"].append(icsv)
            SalmoNet["node"][row[0]]["networkjson"].append(
                { "data": {
                    "id": "%s_%s"%(SalmoNet["node"][row[0]]["name"],SalmoNet["node"][row[1]]["name"]),
                    "source": SalmoNet["node"][row[0]]["name"],
                    "target": SalmoNet["node"][row[1]]["name"],
                    "type": row[3],
                },
            })
            if SalmoNet["node"][row[0]] != SalmoNet["node"][row[1]]:
                SalmoNet["node"][row[1]]["networkjson"].append(
                    { "data": {
                        "id": "%s_%s"%(SalmoNet["node"][row[0]]["name"],SalmoNet["node"][row[1]]["name"]),
                        "source": SalmoNet["node"][row[0]]["name"],
                        "target": SalmoNet["node"][row[1]]["name"],
                        "type": row[3],
                    },
                })

    for node in SalmoNet["node"]:
        SalmoNet["node"][node]["num_ortholog"] = len(SalmoNet["groups"][SalmoNet["node"][node]["group"]])
        SalmoNet["node"][node]["orthologs"] = SalmoNet["groups"][SalmoNet["node"][node]["group"]]
    node0interaction = []
    for node in SalmoNet["node"]:
        if len(SalmoNet["node"][node]["interactions"]) == 0:
            node0interaction.append(node)
    for node in node0interaction:
        del SalmoNet["node"][node]
    return SalmoNet


def export_strain_select_json(SalmoNet, out_file, strains_long_name):
    select = []
    select.append({"value": "Select a strain", "id": 0})
    for id, strain in enumerate(SalmoNet["strains"]):
        select.append({"id": id+1, "value": strains_long_name[strain]})
    with open(out_file, "w") as f:
        json.dump(select, f)


def export_strain_node_lists(SalmoNet, files_prefix):
    for id, strain in enumerate(SalmoNet["strains"]):
        with open("%s/nodes%s.csv" % (files_prefix, id+1), "w") as f:
            for nid, node in enumerate(SalmoNet["node"]):
                if SalmoNet["node"][node]["strain"] == strain:
                    f.write("%s,%s,%s,%s,%s,%s,%s\n" % (
                        nid,
                        node,
                        SalmoNet["node"][node]["name"],
                        SalmoNet["node"][node]["locus"],
                        SalmoNet["node"][node]["old_locus"],
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
            
            md_data["genename"] = SalmoNet["node"][uniprot]["name"]
            md_data["old_locus"] = SalmoNet["node"][uniprot]["old_locus"]
            md_data["locus"] = SalmoNet["node"][uniprot]["locus"]
            md_data["strain"] = SalmoNet["node"][uniprot]["strain"]
            md_data["orthologs"] = SalmoNet["node"][uniprot]["orthologs"]
            md_data["uniprot"] = uniprot
            md_data["interactioncsv"] = "\n".join(SalmoNet["node"][uniprot]["interactions"])
            
            networkjsonnodes = {}
            for n in SalmoNet["node"][uniprot]["networkjson"]:
                if n["data"]["source"] not in networkjsonnodes:
                    networkjsonnodes[n["data"]["source"]] = True
                if n["data"]["target"] not in networkjsonnodes:
                    networkjsonnodes[n["data"]["target"]] = True
            for n in networkjsonnodes.keys():
                if n == SalmoNet["node"][uniprot]["name"]:
                    SalmoNet["node"][uniprot]["networkjson"].append({"data":{"id":n,"main": True}})
                else:
                    SalmoNet["node"][uniprot]["networkjson"].append({"data":{"id":n,"main": False}})
            md_data["networkjson"] = json.dumps(SalmoNet["node"][uniprot]["networkjson"])
            #
            md = yaml.dump(md_data, allow_unicode=True,
                      default_flow_style=False,
                      explicit_start=True, explicit_end=True,
                      default_style="'", line_break="/n")[:-4]
            md += "---\n"
            f.write(md)
        if just_one:
            return
