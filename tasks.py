#!/usr/bin/env python3
from invoke import task
from invoke import Collection
import template.tasks

@task
def test(ctx):
    ctx.run("echo \"main - OK\"")

ns = Collection()
ns.add_task(test)
ns.add_collection(template.tasks, 'template')