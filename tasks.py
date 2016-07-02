#!/usr/bin/env python3
from invoke import task
from invoke import Collection
import template.tasks
import scripts.tasks
import SalmoNet.tasks

@task
def test(ctx):
    ctx.run("echo \"main - OK\"")

ns = Collection()
ns.add_task(test)
ns.add_collection(template.tasks, 'template')
ns.add_collection(scripts.tasks, 'data')
ns.add_collection(SalmoNet.tasks, 'site')
