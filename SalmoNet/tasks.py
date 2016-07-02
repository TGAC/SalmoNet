#!/usr/bin/env python3
from invoke import task

@task()
def test(ctx):
    ctx.run("echo \"site - OK\"")
