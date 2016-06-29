#!/bin/env python3

import csv
import json

strains = []
SalmoNet = {"node": {}, "interaction": {}, "groups": {}}
with open("../data/HC_nodes.csv") as f:
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
        }
        if row[3] not in SalmoNet["groups"]:
            SalmoNet["groups"][row[3]] = []
        SalmoNet["groups"][row[3]].append(row[0])
        if row[4] not in strains:
            strains.append(row[4])

with open("../data/HC_interactions.csv") as f:
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

for node in SalmoNet["node"]:
    SalmoNet["node"][node]["num_ortholog"] = len(SalmoNet["groups"][SalmoNet["node"][node]["group"]])

nn = 1
for s in strains:
    with open("../template/src/data/nodes%s.csv" % nn, "w") as f:
        n = 0
        for node in SalmoNet["node"]:
            if SalmoNet["node"][node]["strain"] == s:
                f.write("%s,%s,%s,%s,%s,%s,%s\n" % (
                    n,
                    node,
                    SalmoNet["node"][node]["name"],
                    SalmoNet["node"][node]["locus"],
                    SalmoNet["node"][node]["strain"],
                    SalmoNet["node"][node]["num_ortholog"],
                    SalmoNet["node"][node]["num_interaction"],
                ))
                n += 1
    nn += 1